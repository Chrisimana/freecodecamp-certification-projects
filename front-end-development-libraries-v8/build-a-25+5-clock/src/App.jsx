import React, { useEffect, useRef, useState } from 'react';

const INITIAL_BREAK = 5;
const INITIAL_SESSION = 25;
const MIN_LENGTH = 1;
const MAX_LENGTH = 60;

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainder = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainder}`;
}

function App() {
  const [breakLength, setBreakLength] = useState(INITIAL_BREAK);
  const [sessionLength, setSessionLength] = useState(INITIAL_SESSION);
  const [mode, setMode] = useState('Session');
  const [timeLeft, setTimeLeft] = useState(INITIAL_SESSION * 60);
  const [isRunning, setIsRunning] = useState(false);
  const beepRef = useRef(null);

  useEffect(() => {
    if (!isRunning) return undefined;

    const interval = window.setInterval(() => {
      setTimeLeft((current) => {
        if (current > 0) return current - 1;

        const beep = beepRef.current;
        if (beep) {
          beep.currentTime = 0;
          void beep.play().catch(() => {});
        }

        setMode((currentMode) => {
          const nextMode = currentMode === 'Session' ? 'Break' : 'Session';
          setTimeLeft((nextMode === 'Session' ? sessionLength : breakLength) * 60);
          return nextMode;
        });
        return 0;
      });
    }, 1000);

    return () => window.clearInterval(interval);
  }, [isRunning, breakLength, sessionLength]);

  const changeLength = (type, amount) => {
    if (isRunning) return;
    const setter = type === 'break' ? setBreakLength : setSessionLength;
    setter((current) => Math.min(MAX_LENGTH, Math.max(MIN_LENGTH, current + amount)));
    if (type === 'session') setTimeLeft((current) => current === sessionLength * 60 ? Math.min(MAX_LENGTH, Math.max(MIN_LENGTH, sessionLength + amount)) * 60 : current);
  };

  const reset = () => {
    setIsRunning(false);
    setBreakLength(INITIAL_BREAK);
    setSessionLength(INITIAL_SESSION);
    setMode('Session');
    setTimeLeft(INITIAL_SESSION * 60);
    if (beepRef.current) {
      beepRef.current.pause();
      beepRef.current.currentTime = 0;
    }
  };

  return (
    <main className="app-shell">
      <section className="clock-card" aria-label="25 plus 5 clock">
        <p className="kicker">A QUIET RHYTHM FOR DEEP WORK</p>
        <h1>Focus / Rest</h1>

        <div className="timer-panel">
          <div className="timer-heading">
            <span className="status-dot" aria-hidden="true" />
            <span id="timer-label">{mode}</span>
          </div>
          <div id="time-left" className={timeLeft < 60 ? 'time-left urgent' : 'time-left'}>{formatTime(timeLeft)}</div>
          <div className="timer-actions">
            <button id="start_stop" className="primary-button" onClick={() => setIsRunning((running) => !running)}>
              {isRunning ? 'Pause' : 'Start'}
            </button>
            <button id="reset" className="text-button" onClick={reset}>Reset</button>
          </div>
        </div>

        <div className="length-controls">
          <LengthControl id="break" label="Break Length" value={breakLength} onChange={changeLength} />
          <LengthControl id="session" label="Session Length" value={sessionLength} onChange={changeLength} />
        </div>

        <p className="hint">Intervals alternate automatically. Find your pace.</p>
        <audio id="beep" ref={beepRef} preload="auto" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" />
      </section>
    </main>
  );
}

function LengthControl({ id, label, value, onChange }) {
  return (
    <div className="length-control">
      <span id={`${id}-label`} className="control-label">{label}</span>
      <div className="stepper">
        <button id={`${id}-decrement`} aria-label={`Decrease ${label}`} onClick={() => onChange(id, -1)}>−</button>
        <span id={`${id}-length`} className="length-value">{value}</span>
        <button id={`${id}-increment`} aria-label={`Increase ${label}`} onClick={() => onChange(id, 1)}>+</button>
      </div>
    </div>
  );
}

export default App;
