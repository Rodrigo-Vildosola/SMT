# Title slide
## subtitle

***

## first slide

- bullet 1
- bullet 2
- bullet 3

***

## second slide

```rawhtml
<div>This HTML will be <em>injected</em> directly</div>
```


### Building the Presentation

To convert your markdown file into a presentation, you would run the build command provided by `markdown-to-presentation`. This command would take your `slides.md` and turn it into an HTML presentation using `reveal.js`, applying the styles defined in your SCSS files.

### Publishing to GitHub Pages

Once the presentation is built, you can publish it to GitHub Pages by pushing the build directory to the `gh-pages` branch of your repository. This will make the presentation accessible as a live website.

### Workflow Summary

1. **Write your slides**: Create a `slides.md` file with the content of your presentation.
2. **Customize styles**: Modify `_theme.scss` and `_app.scss` to customize the look of your presentation.
3. **Build the presentation**: Use the tool to convert your markdown into an HTML presentation.
4. **Publish**: Deploy the presentation to GitHub Pages by pushing to the `gh-pages` branch.

### Additional Notes

- **Horizontal Rules**: The slide delimiter is `***`, so if you need a horizontal rule in your slides, use `---` or `___` instead.
- **Raw HTML**: You can inject raw HTML into your slides by using a `rawhtml` code block.

This setup makes it easy to maintain and publish presentations using markdown, allowing for flexibility and ease of use. If you have any specific questions about using this tool or need further assistance with a step, feel free to ask!
