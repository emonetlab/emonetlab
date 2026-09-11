require 'json'
require 'mini_magick'

module Jekyll
  # Publish one complete photo page and viewer manifest per album.
  class GalleryGenerator < Generator
    safe true
    priority :low

    IMAGE_EXTENSIONS = %w[.jpg .jpeg .png .gif .webp].freeze
    VIEWER_ASSETS = %w[
      lightgallery.min.js plugins/zoom/lg-zoom.min.js
      css/lightgallery.css css/lg-zoom.css
      fonts/lg.woff2 fonts/lg.woff fonts/lg.ttf fonts/lg.svg images/loading.gif
    ].freeze

    def generate(site)
      copy_viewer_assets(site)
      entries = site.data['gallery']
      unless entries.is_a?(Array) && !entries.empty?
        raise Errors::FatalException, 'Gallery: _data/gallery.yml must list at least one published album.'
      end

      ids = entries.map { |entry| entry.is_a?(Hash) && entry['id'] }
      unless ids.all? { |id| id.is_a?(String) && id.match?(/\A\d{4}-\d{4}\z/) } && ids.uniq == ids
        raise Errors::FatalException, 'Gallery: each album needs a unique id in YYYY-YYYY format.'
      end

      albums = entries.map { |entry| read_album(site, entry) }
      albums.each_with_index do |album, index|
        album['newer'] = album_link(albums[index - 1]) if index.positive?
        album['older'] = album_link(albums[index + 1]) if index + 1 < albums.length
        generate_page(site, album)
        generate_manifest(site, album)
      end
      site.data['gallery_albums'] = albums
    end

    private

    def copy_viewer_assets(site)
      VIEWER_ASSETS.each do |asset|
        relative_path = "node_modules/lightgallery/#{asset}"
        unless File.file?(File.join(site.source, relative_path))
          raise Errors::FatalException, "Gallery: missing #{relative_path}. Run npm ci before building the site."
        end
        next if site.static_files.any? { |file| file.relative_path.delete_prefix('/') == relative_path }

        site.static_files << StaticFile.new(site, site.source, File.dirname(relative_path), File.basename(relative_path))
      end
    end

    def album_link(album)
      album.slice('id', 'title', 'url')
    end

    def read_album(site, entry)
      id = entry['id']
      title = id.tr('-', '–')
      directory = File.join(site.source, 'assets/images/gallery', id)
      filenames = Dir.glob(File.join(directory, '*')).select do |filename|
        File.file?(filename) && IMAGE_EXTENSIONS.include?(File.extname(filename))
      end.map { |filename| File.basename(filename) }.sort
      if filenames.empty?
        raise Errors::FatalException, "Gallery: album #{id} has no supported images in #{directory}."
      end
      unless filenames.include?(entry['cover'])
        raise Errors::FatalException, "Gallery: cover #{entry['cover'].inspect} is missing from album #{id}."
      end

      details = site.data.fetch('galleries', {}).fetch("#{id}_details", [])
      photos = filenames.each_with_index.map do |filename, index|
        metadata = details.find { |detail| detail['filename'] == filename } || {}
        image = MiniMagick::Image.new(File.join(directory, filename))
        width, height = image.dimensions
        # Derivatives are auto-oriented, so reserve their displayed geometry.
        width, height = height, width if %w[LeftTop RightTop RightBottom LeftBottom].include?(image['%[orientation]'])
        caption = metadata.fetch('caption', '').to_s
        alt = metadata['alt'].to_s
        alt = caption.empty? ? "Photo #{index + 1} from the #{title} album" : caption if alt.empty?
        {
          'filename' => filename,
          'caption' => caption,
          'alt' => alt,
          'original' => "/assets/images/gallery/#{id}/#{filename}",
          'preview' => "/gallery-images/preview/#{id}/#{filename}.webp",
          'viewer' => "/gallery-images/viewer/#{id}/#{filename}.webp",
          'width' => width,
          'height' => height,
          'index' => index
        }
      end
      {
        'id' => id,
        'title' => title,
        'url' => "/gallery/#{id}/",
        'count' => photos.length,
        'cover' => photos.find { |photo| photo['filename'] == entry['cover'] },
        'photos' => photos,
        'manifest_url' => "/gallery/#{id}/photos.json",
        'newer' => nil,
        'older' => nil
      }
    end

    def generate_page(site, album)
      page = PageWithoutAFile.new(site, site.source, album['url'].delete_prefix('/'), 'index.html')
      page.content = ''
      page.data.merge!(
        'layout' => 'gallery-album',
        'gallery' => true,
        'title' => album['title'],
        'description' => "#{album['count']} photos from lab life.",
        'background' => { 'img' => '/assets/backgrounds/AdobeStock_561560383.jpeg', 'by' => 'Adobe' },
        'album' => album,
        'photos' => album['photos']
      )
      site.pages << page
    end

    def generate_manifest(site, album)
      page = PageWithoutAFile.new(site, site.source, "gallery/#{album['id']}", 'photos.json')
      # A caption can contain Liquid syntax. JSON must preserve it as plain text.
      page.data.merge!('layout' => nil, 'render_with_liquid' => false, 'sitemap' => false)
      page.content = JSON.generate(album.slice('id', 'title', 'photos'))
      site.pages << page
    end
  end
end
