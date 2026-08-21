import { StrictMode, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { marked } from 'marked'
import './styles.css'

const starterMarkdown = `# Ink & Render

## A small space for clear ideas

Write in **Markdown** and watch it become a polished document. Try a [useful link](https://developer.mozilla.org/en-US/docs/Web/JavaScript), some \`inline code\`, or a code block:

\`\`\`js
const hello = 'beautifully rendered';
console.log(hello);
\`\`\`

> Good writing leaves a little room for the reader.

- Keep ideas simple
- Give them shape

![A quiet mountain landscape](https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=80)

**Make something worth reading.**`

marked.setOptions({ breaks: true, gfm: true })

function App() {
  const [markdown, setMarkdown] = useState(starterMarkdown)
  const renderedMarkdown = useMemo(() => marked.parse(markdown), [markdown])

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <span className="brand-mark" aria-hidden="true">✦</span>
          <div>
            <p className="eyebrow">A quiet writing tool</p>
            <h1>Ink <span>&</span> Render</h1>
          </div>
        </div>
        <p className="live-status"><span className="status-dot" /> Live preview</p>
      </header>

      <section className="workspace" aria-label="Markdown editor and preview">
        <article className="panel editor-panel">
          <div className="panel-heading">
            <div>
              <span className="panel-index">01</span>
              <h2>Write</h2>
            </div>
            <span className="panel-note">Markdown</span>
          </div>
          <label className="sr-only" htmlFor="editor">Markdown editor</label>
          <textarea
            id="editor"
            value={markdown}
            onChange={(event) => setMarkdown(event.target.value)}
            spellCheck="false"
            aria-label="Markdown editor"
          />
          <div className="editor-footer">
            <span>{markdown.length} characters</span>
            <span>GFM enabled</span>
          </div>
        </article>

        <article className="panel preview-panel">
          <div className="panel-heading">
            <div>
              <span className="panel-index">02</span>
              <h2>Read</h2>
            </div>
            <span className="panel-note">Rendered HTML</span>
          </div>
          <div id="preview" className="markdown-body" dangerouslySetInnerHTML={{ __html: renderedMarkdown }} />
        </article>
      </section>

      <footer className="page-footer">
        <span>Crafted for the curious mind</span>
        <span className="footer-line" />
        <span>Write freely. Preview instantly.</span>
      </footer>
    </main>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
