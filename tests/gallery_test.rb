require 'jekyll'
require 'json'
require 'tmpdir'
require 'fileutils'
require 'yaml'

repo = File.expand_path('..', __dir__)
require File.join(repo, '_plugins/gallery.rb')
require File.join(repo, '_plugins/jekyll_minimagick.rb')
def check(condition, message)
  raise message unless condition
end

# Updating one source must refresh every preset, independent of write order.
Dir.mktmpdir('gallery-derivatives-') do |scratch|
  FileUtils.mkdir_p(File.join(scratch, 'photos'))
  source = File.join(scratch, 'photos', 'sample.png')
  system('magick', '-size', '4x4', 'xc:red', source, exception: true)
  old_time = Time.at(1_600_000_000)
  File.utime(old_time, old_time, source)
  presets = %w[preview viewer].to_h do |name|
    [name, {
      'source' => 'photos', 'destination' => "derivatives/#{name}",
      'format' => 'webp', 'auto_orient' => true, 'resize' => '2x2',
      'strip' => true, 'quality' => 100
    }]
  end
  fixture = Jekyll::Site.new(Jekyll.configuration(
    'source' => scratch, 'destination' => File.join(scratch, '_site'),
    'mini_magick' => presets, 'quiet' => true
  ))
  generate_outputs = lambda do
    fixture.static_files.clear
    Dir.chdir(scratch) { Jekyll::JekyllMinimagick::MiniMagickGenerator.new.generate(fixture) }
    fixture.static_files
  end
  outputs = generate_outputs.call
  check(outputs.length == 2, 'two image presets are generated')
  check(outputs.map { |image| image.write(fixture.dest) } == [true, true], 'both initial derivatives are written')
  check(generate_outputs.call.map { |image| image.write(fixture.dest) } == [false, false], 'unchanged derivatives are skipped')

  outputs.each do |image|
    destination = image.destination(fixture.dest)
    File.utime(old_time, old_time, destination)
  end
  system('magick', '-size', '4x4', 'xc:blue', source, exception: true)
  source_time = Time.now
  File.utime(source_time, source_time, source)
  outputs = generate_outputs.call
  check(outputs.map { |image| image.write(fixture.dest) } == [true, true], 'a replaced source refreshes both derivatives')
  outputs.each do |image|
    pixel = MiniMagick::Image.new(image.destination(fixture.dest)).get_pixels.first.first
    check(pixel[2] > pixel[0], 'each derivative contains the replacement blue image')
  end
  check(generate_outputs.call.map { |image| image.write(fixture.dest) } == [false, false], 'both refreshed derivatives are skipped without another change')
  puts 'Derivatives: both presets refresh a replaced photo, preserve its new pixels, and skip unchanged outputs.'
end

site = Jekyll::Site.new(Jekyll.configuration('source' => repo, 'destination' => File.join(Dir.tmpdir, 'gallery-generator-check'), 'quiet' => true))
site.read
Jekyll::GalleryGenerator.new.generate(site)
albums = site.data.fetch('gallery_albums')
expected_ids = YAML.load_file(File.join(repo, '_data/gallery.yml')).map { |entry| entry['id'] }
check(albums.map { |album| album['id'] } == expected_ids, 'only explicitly published albums are included')
pages = site.pages.select { |page| page.data['layout'] == 'gallery-album' }
check(pages.length == albums.length, 'each album has exactly one page')
check(pages.all? { |page| page.data['photos'] == page.data['album']['photos'] }, 'each album page contains all its photos')
check(pages.sum { |page| page.data['photos'].length } == albums.sum { |album| album['count'] }, 'every published photo has a page')
check(albums.first['newer'].nil? && albums.last['older'].nil?, 'neighbor bounds')
check(site.static_files.count { |file| file.relative_path.delete_prefix('/').start_with?('node_modules/lightgallery/') } == 9, 'viewer dependencies')
puts 'Published albums: single pages, complete photo collections, neighboring links, and viewer assets passed.'

Dir.mktmpdir('gallery-fixture-') do |scratch|
  FileUtils.mkdir_p(File.join(scratch, 'assets/images/gallery/2099-2100'))
  FileUtils.mkdir_p(File.join(scratch, 'node_modules'))
  File.symlink(File.join(repo, 'node_modules/lightgallery'), File.join(scratch, 'node_modules/lightgallery'))
  source = File.join(scratch, 'tiny.png')
  system('magick', '-size', '2x2', 'xc:white', source, exception: true)
  200.times { |index| File.symlink(source, File.join(scratch, 'assets/images/gallery/2099-2100', format('%03d.png', index))) }
  fixture = Jekyll::Site.new(Jekyll.configuration('source' => scratch, 'destination' => File.join(scratch, '_site'), 'quiet' => true))
  fixture.data['gallery'] = [{ 'id' => '2099-2100', 'cover' => '000.png' }]
  literal_caption = '{{ site.title }} <b>literal & caption</b>'
  fixture.data['galleries'] = {'2099-2100_details' => [{'filename' => '000.png', 'caption' => literal_caption}]}
  Jekyll::GalleryGenerator.new.generate(fixture)
  photo_pages = fixture.pages.select { |page| page.data['layout'] == 'gallery-album' }
  check(photo_pages.length == 1, '200 photos remain on one album page')
  check(photo_pages.first.url == '/gallery/2099-2100/', 'single album route')
  check(!photo_pages.first.data.key?('pagination'), 'album has no pagination state')
  check(photo_pages.flat_map { |page| page.data['photos'].map { |photo| photo['index'] } } == (0...200).to_a, 'each photo occurs once in deterministic order')
  manifest = fixture.pages.find { |page| page.name == 'photos.json' }
  check(JSON.parse(manifest.content)['photos'].length == 200, 'manifest includes all photos')
  check(JSON.parse(manifest.content)['photos'].first['caption'] == literal_caption, 'manifest preserves literal captions')
  check(manifest.data['render_with_liquid'] == false && manifest.data['layout'].nil?, 'manifest rendering bypass')
  check(JSON.parse(manifest.content)['photos'].first['viewer'].end_with?('/000.png.webp'), 'derivative naming matches plugin')
  fixture.data['gallery'].first['cover'] = 'missing.png'
  begin
    Jekyll::GalleryGenerator.new.generate(fixture)
    raise 'missing cover accepted'
  rescue Jekyll::Errors::FatalException => error
    check(error.message.include?('cover "missing.png" is missing'), 'missing-cover diagnosis')
  end
  fixture.data['gallery'] = [{'id' => '2080-2081', 'cover' => 'none.png'}]
  begin
    Jekyll::GalleryGenerator.new.generate(fixture)
    raise 'empty album accepted'
  rescue Jekyll::Errors::FatalException => error
    check(error.message.include?('has no supported images'), 'empty-album diagnosis')
  end
  fixture.data['gallery'] = [{'id' => '2099-2100', 'cover' => '000.png'}] * 2
  begin
    Jekyll::GalleryGenerator.new.generate(fixture)
    raise 'duplicate ID accepted'
  rescue Jekyll::Errors::FatalException => error
    check(error.message.include?('unique id'), 'duplicate-ID diagnosis')
  end
  puts 'Fixture: all 200 photos appear on one page; exact ordering, JSON, cover, empty-album and duplicate-ID checks passed.'
end
