import { useState } from 'react'
import './App.css'

const numberButtons = [
  ['seven', '7'],
  ['eight', '8'],
  ['nine', '9'],
  ['four', '4'],
  ['five', '5'],
  ['six', '6'],
  ['one', '1'],
  ['two', '2'],
  ['three', '3'],
  ['zero', '0'],
]

const operatorButtons = [
  ['add', '+'],
  ['subtract', '-'],
  ['multiply', '*'],
  ['divide', '/'],
]

const isOperator = (value) => /[+*/-]/.test(value)

function App() {
  const [expression, setExpression] = useState('0')
  const [display, setDisplay] = useState('0')
  const [evaluated, setEvaluated] = useState(false)

  const appendNumber = (value) => {
    if (evaluated) {
      setExpression(value)
      setDisplay(value)
      setEvaluated(false)
      return
    }

    const parts = expression.split(/[+*/-]/)
    const currentNumber = parts.at(-1)
    const nextExpression = currentNumber === '0' ? expression.slice(0, -1) + value : expression + value
    setExpression(nextExpression)
    setDisplay(nextExpression)
  }

  const appendDecimal = () => {
    if (evaluated) {
      setExpression('0.')
      setDisplay('0.')
      setEvaluated(false)
      return
    }

    const currentNumber = expression.split(/[+*/-]/).at(-1)
    if (!currentNumber.includes('.')) {
      const nextExpression = expression === '0' ? '0.' : expression + '.'
      setExpression(nextExpression)
      setDisplay(nextExpression)
    }
  }

  const appendOperator = (operator) => {
    if (evaluated) {
      setExpression(display + operator)
      setDisplay(display + operator)
      setEvaluated(false)
      return
    }

    if (expression === '0' && operator !== '-') return
    const lastCharacter = expression.at(-1)
    if (isOperator(lastCharacter)) {
      if (operator === '-' && lastCharacter !== '-') {
        setExpression(expression + operator)
        setDisplay(expression + operator)
      } else if (lastCharacter === '-' && expression.length > 1 && isOperator(expression.at(-2))) {
        const nextExpression = expression.slice(0, -2) + operator
        setExpression(nextExpression)
        setDisplay(nextExpression)
      } else {
        const nextExpression = expression.slice(0, -1) + operator
        setExpression(nextExpression)
        setDisplay(nextExpression)
      }
      return
    }

    setExpression(expression + operator)
    setDisplay(expression + operator)
  }

  const calculate = () => {
    if (isOperator(expression.at(-1))) return
    try {
      const result = Function(`"use strict"; return (${expression})`)()
      const formattedResult = Number.isFinite(result) ? String(Number(result.toFixed(10))) : 'Error'
      setExpression(formattedResult)
      setDisplay(formattedResult)
      setEvaluated(true)
    } catch {
      setExpression('Error')
      setDisplay('Error')
      setEvaluated(true)
    }
  }

  const clear = () => {
    setExpression('0')
    setDisplay('0')
    setEvaluated(false)
  }

  return (
    <main className="app-shell">
      <section className="calculator" aria-label="JavaScript calculator">
        <header className="calculator-header">
          <div>
            <p className="eyebrow">React utility</p>
            <h1>Calculate.</h1>
          </div>
          <span className="status-dot" aria-label="Ready" />
        </header>
        <div className="screen" aria-live="polite">
          <span className="expression">{evaluated ? 'Result' : 'Input'}</span>
          <output id="display">{display}</output>
        </div>
        <div className="keypad">
          <button id="clear" className="key key-clear" onClick={clear}>AC</button>
          {operatorButtons.map(([id, label]) => (
            <button id={id} className="key key-operator" onClick={() => appendOperator(label)} key={id}>{label}</button>
          ))}
          {numberButtons.map(([id, label]) => (
            <button id={id} className={`key ${id === 'zero' ? 'key-zero' : ''}`} onClick={() => appendNumber(label)} key={id}>{label}</button>
          ))}
          <button id="decimal" className="key" onClick={appendDecimal}>.</button>
          <button id="equals" className="key key-equals" onClick={calculate}>=</button>
        </div>
      </section>
      <p className="footer-note">Simple tools for clear thinking</p>
    </main>
  )
}

export default App
