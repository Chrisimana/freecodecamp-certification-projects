import { useState } from 'react'
import './App.css'

const quotes = [
  {
    text: 'The future belongs to those who believe in the beauty of their dreams.',
    author: 'Eleanor Roosevelt',
  },
  {
    text: 'Do what you feel in your heart to be right, for you will be criticized anyway.',
    author: 'Eleanor Roosevelt',
  },
  {
    text: 'Great things are done by a series of small things brought together.',
    author: 'Vincent van Gogh',
  },
  {
    text: 'It always seems impossible until it is done.',
    author: 'Nelson Mandela',
  },
  {
    text: 'The only way to do great work is to love what you do.',
    author: 'Steve Jobs',
  },
]

function getRandomQuote(currentQuote) {
  const availableQuotes = quotes.filter((quote) => quote !== currentQuote)
  return availableQuotes[Math.floor(Math.random() * availableQuotes.length)]
}

function App() {
  const [quote, setQuote] = useState(() => quotes[Math.floor(Math.random() * quotes.length)])

  const showNewQuote = () => setQuote((currentQuote) => getRandomQuote(currentQuote))
  const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
    `"${quote.text}" - ${quote.author}`,
  )}`

  return (
    <main className="app-shell">
      <header className="masthead">
        <p className="eyebrow">A small pause for a big thought</p>
        <h1>Daily <span>muse</span></h1>
      </header>

      <section id="quote-box" className="quote-card" aria-live="polite">
        <div className="quote-mark" aria-hidden="true">“</div>
        <blockquote>
          <p id="text">{quote.text}</p>
          <cite id="author">— {quote.author}</cite>
        </blockquote>
        <div className="quote-actions">
          <a
            id="tweet-quote"
            className="tweet-link"
            href={tweetUrl}
            target="_blank"
            rel="noreferrer"
            aria-label="Tweet this quote"
          >
            <span aria-hidden="true">♥</span> Share the thought
          </a>
          <button id="new-quote" type="button" onClick={showNewQuote}>
            New quote <span aria-hidden="true">↗</span>
          </button>
        </div>
      </section>

      <footer>WORDS TO CARRY WITH YOU <span>•</span> 01 / 05</footer>
    </main>
  )
}

export default App
