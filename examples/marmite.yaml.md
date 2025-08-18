# Marmite Blog Configuration

You can configure your Marmite blog using the `marmite.yaml` file,
this document explains each variable and the documentation here is available
on your code editor with `doc-lsp`.

Open the `marmite.yaml` on your editor and trigger the `view_doc` action on any variable.

## name
> The name of your blog, this shows on the top of the page.

## tagline
> The tagline of your blog, this shows on the top of the page.

## url
> The URL of your blog, this is used to generate the RSS feed and other links.

## https
> Whether to use HTTPS, this is used to generate the RSS feed and other links.

## footer
> The footer of your blog, this shows at the bottom of the page.

## language
> The language of your blog, this is used to determine the language of the blog.

## pagination = 10
> The number of posts per page, this is used to determine the number of posts per page.

## pages_title = Pages
> The title of the pages page, this is used to determine the title of the pages page.

## tags_title = Tags
> The title of the tags page, this is used to determine the title of the tags page.

## tags_content_title = Posts tagged with '$tag'
> The content title of the tags page, this is used to determine the content title of the tags page. `$tag` is replaced with the name of the tag.

## archives_title = Archive
> The title of the archives page, this is used to determine the title of the archives page.

## archives_content_title = Posts from '$year'
> The content title of the archives page, this is used to determine the content title of the archives page. `$year` is replaced with the year of the post.

## streams_title = Streams
> The title of the streams page, this is used to determine the title of the streams page.

## streams_content_title = Posts from '$stream'
> The content title of the streams page, this is used to determine the content title of the streams page. `$stream` is replaced with the name of the stream.

## series_title = Series
> The title of the series page, this is used to determine the title of the series page.

## series_content_title = Posts from '$series' series
> The content title of the series page, this is used to determine the content title of the series page. `$series` is replaced with the name of the series.

## default_author
> The default author of your blog, this is used to determine the default author of the blog. If empty, the first author in the `authors` list will be used.

## authors_title = Authors
> The title of the authors page, this is used to determine the title of the authors page.

## enable_search = false
> Whether to enable search.

## enable_related_content = false
> Whether to enable related content.

## search_title
> The title of the search page.

## content_path = content
> The path to the content of your blog.

## site_path = site
> The path to the site of your blog.

## templates_path = templates
> The path to the templates of your blog.

## static_path = static
> The path to the static of your blog.

## media_path = media
> The path to the media of your blog.

## card_image
> The card image of your blog.

## banner_image
> The banner image of your blog.

## logo_image    
> The logo image of your blog.

## default_date_format = '%b %e, %Y'
> The default date format of your blog.

## menu
>>>
The menu of your blog, this is used to determine the menu of the blog, this is a list of tuples, each tuple contains a title and a path.

Example:

```yaml
menu:
- - Tags
  - tags.html
```
>>>

## extra
> Extra configuration for your blog, this accepts any key-value 
> pair and can be used by themes to refer to extra data, the actual
> data will depend on the theme you are using.


## authors
>>>
The authors of the blog, this is a dictionary of authors, the key is the author's name and the value is a dictionary of author's data.

Example:

```yaml
authors:
  - name: John Doe
    email: john.doe@example.com
```

The `name` is the author's name, the `email` is the author's email, the `url` is the author's URL, the `avatar` is the author's avatar, the `bio` is the author's bio.

>>>

### authors[item].name
> The name of the author.

### authors[item].email
> The email of the author.

### [item].url
> The URL of the author.

### [item].avatar
> The avatar of the author.

### authors[item].bio
> The bio of the author.
