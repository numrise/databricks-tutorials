# MkDocs Configuration

This site is built with MkDocs and the Read the Docs theme.

## Building Locally

### Install MkDocs
```bash
pip install mkdocs mkdocs-material
```

### Serve Documentation
```bash
mkdocs serve
```

Then open http://localhost:8000

## Building for GitHub Pages

```bash
mkdocs build
```

The site will be generated in the `site/` directory.

## Deployment

Push to GitHub and enable GitHub Pages to serve from the `gh-pages` branch.
