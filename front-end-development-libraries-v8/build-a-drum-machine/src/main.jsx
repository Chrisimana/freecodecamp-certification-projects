import React, { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom';
import './styles.css';

const pads = [
  { key: 'Q', name: 'Heater 1', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Heater-1.mp3' },
  { key: 'W', name: 'Heater 2', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Heater-2.mp3' },
  { key: 'E', name: 'Heater 3', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Heater-3.mp3' },
  { key: 'A', name: 'Heater 4', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Heater-4_1.mp3' },
  { key: 'S', name: 'Clap', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Heater-6.mp3' },
  { key: 'D', name: 'Open HH', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Dsc_Oh.mp3' },
  { key: 'Z', name: "Kick n' Hat", audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Kick_n_Hat.mp3' },
  { key: 'X', name: 'Kick', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/RP4_KICK_1.mp3' },
  { key: 'C', name: 'Closed HH', audio: 'https://cdn.freecodecamp.org/testable-projects-fcc/audio/Cev_H2.mp3' },
];

function DrumPad({ pad, onTrigger, registerAudio }) {
  const [active, setActive] = useState(false);

  const play = () => {
    const audio = registerAudio(pad.key);
    if (!audio) return;
    audio.currentTime = 0;
    audio.play();
    setActive(true);
    window.setTimeout(() => setActive(false), 120);
    onTrigger(pad.name);
  };

  return (
    <button className={`drum-pad${active ? ' active' : ''}`} id={pad.name.replace(/[^a-z0-9]/gi, '-').toLowerCase()} onClick={play} type="button">
      <span className="pad-key">{pad.key}</span>
      <span className="pad-name">{pad.name}</span>
      <audio className="clip" id={pad.key} ref={(audio) => registerAudio(pad.key, audio)} src={pad.audio} preload="auto" />
    </button>
  );
}

function DrumMachine() {
  const audioMap = useRef({});
  const [display, setDisplay] = useState('Select a pad');

  const registerAudio = (key, audio) => {
    if (audio) audioMap.current[key] = audio;
    return audioMap.current[key];
  };

  const triggerKey = (key) => {
    const pad = pads.find((item) => item.key === key);
    if (pad) document.getElementById(pad.key)?.parentElement?.click();
  };

  useEffect(() => {
    const handleKeyDown = (event) => triggerKey(event.key.toUpperCase());
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <main id="drum-machine">
      <section className="machine-shell" aria-label="Pulse drum machine">
        <header className="machine-header">
          <div>
            <p className="eyebrow">RHYTHM LAB / 09</p>
            <h1>Pulse</h1>
          </div>
          <div className="status"><span /> LIVE</div>
        </header>
        <div className="display-panel">
          <span className="display-label">NOW PLAYING</span>
          <div id="display">{display}</div>
        </div>
        <div className="pads" aria-label="Drum pads">
          {pads.map((pad) => <DrumPad key={pad.key} pad={pad} onTrigger={setDisplay} registerAudio={registerAudio} />)}
        </div>
        <footer><span>PRESS A KEY</span><span>Q W E / A S D / Z X C</span></footer>
      </section>
    </main>
  );
}

ReactDOM.render(<DrumMachine />, document.getElementById('root'));
