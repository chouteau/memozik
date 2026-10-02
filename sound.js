/**
 * MemoZik - Moteur Audio Web Audio API & Synthétiseur Musical Haute Fidélité
 * 100% natif, zéro dépendance externe, zéro latence, compatible hors-ligne.
 *
 * Améliorations Studio & Acoustique :
 * 1. Réverbération algorithmique stéréo (Concert Hall / Salle boisée chaleureuse)
 * 2. Chaîne de mastering avec égalisation anti-nasillarde (creux à 1.7kHz, boost chaleur à 150Hz)
 * 3. Compresseur multibande / dynamique de mastering pour lier les voix
 * 4. Tables d'ondes acoustiques (PeriodicWave) pour le piano de concert, les cordes et la basse
 * 5. Simulation de choeur de cordes (léger désaccordage ±1.5 cents pour l'effet de trichorde de piano)
 * 6. Attaque de marteau feutré sur les notes de piano
 */

const SoundEngine = {
    ctx: null,
    isMuted: false,

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    },

    toggleMute() {
        this.isMuted = !this.isMuted;
        try {
            localStorage.setItem('memozik_muted', this.isMuted ? 'true' : 'false');
        } catch (e) {}
        if (MusicPlayer) {
            MusicPlayer.setMuted(this.isMuted);
        }
        return this.isMuted;
    },

    loadMuteState() {
        try {
            const saved = localStorage.getItem('memozik_muted');
            if (saved !== null) {
                this.isMuted = saved === 'true';
            }
        } catch (e) {}
        return this.isMuted;
    },

    playCorrect() {
        if (this.isMuted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc1 = this.ctx.createOscillator();
        const osc2 = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc1.type = 'sine';
        osc2.type = 'triangle';

        // Accord parfait majeur ascendant soyeux : C5 -> E5 -> G5 -> C6
        osc1.frequency.setValueAtTime(523.25, now);
        osc1.frequency.setValueAtTime(659.25, now + 0.08);
        osc1.frequency.setValueAtTime(783.99, now + 0.16);
        osc1.frequency.setValueAtTime(1046.50, now + 0.24);

        osc2.frequency.setValueAtTime(1046.50, now);
        osc2.frequency.setValueAtTime(1318.51, now + 0.08);
        osc2.frequency.setValueAtTime(1567.98, now + 0.16);
        osc2.frequency.setValueAtTime(2093.00, now + 0.24);

        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(this.ctx.destination);

        osc1.start(now);
        osc2.start(now);
        osc1.stop(now + 0.5);
        osc2.stop(now + 0.5);
    },

    playWrong() {
        if (this.isMuted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const filter = this.ctx.createBiquadFilter();
        const gain = this.ctx.createGain();

        osc.type = 'sawtooth';
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(600, now);

        osc.frequency.setValueAtTime(240, now);
        osc.frequency.setValueAtTime(170, now + 0.15);

        gain.gain.setValueAtTime(0.13, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.45);
    },

    playClick() {
        if (this.isMuted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(480, now);
        osc.frequency.exponentialRampToValueAtTime(960, now + 0.035);

        gain.gain.setValueAtTime(0.04, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.04);
    },

    playFanfare() {
        if (this.isMuted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const notes = [
            { f: 523.25, t: 0.00, d: 0.12 }, // C5
            { f: 659.25, t: 0.12, d: 0.12 }, // E5
            { f: 783.99, t: 0.24, d: 0.12 }, // G5
            { f: 1046.50, t: 0.36, d: 0.55 } // C6
        ];

        notes.forEach(note => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(note.f, now + note.t);

            gain.gain.setValueAtTime(0.14, now + note.t);
            gain.gain.exponentialRampToValueAtTime(0.001, now + note.t + note.d);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now + note.t);
            osc.stop(now + note.t + note.d);
        });
    }
};

/**
 * MusicPlayer - Moteur de synthèse Studio Haute Fidélité
 * Transforme les notes MIDI en sonorités acoustiques soyeuses et spatialisées.
 */
const MusicPlayer = {
    ctx: null,
    voiceBus: null,         // Bus d'entrée recevant toutes les voix
    masterGain: null,       // Contrôle de volume principal
    analyser: null,         // Analyseur FFT pour le visualiseur vinyle
    reverbNode: null,       // Convolver de réverbération de concert hall
    dryGain: null,
    wetGain: null,

    // Chaîne d'égalisation de mastering
    warmthEQ: null,
    antiNasalEQ: null,
    smoothAirEQ: null,
    masterCompressor: null,

    // Tables d'ondes acoustiques personnalisées
    pianoWave: null,
    stringsWave: null,
    bassWave: null,
    brassWave: null,

    currentTrack: null,
    isPlaying: false,
    startTime: 0,
    pauseOffset: 0,
    duration: 45,
    volume: 0.8,
    isMuted: false,

    schedulerInterval: null,
    nextNoteIndex: 0,
    activeVoices: [],

    noiseBuffer: null,

    onPlayStateChange: null,
    onTimeUpdate: null,
    onTrackEnd: null,

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (!this.ctx) return;

        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        if (!this.voiceBus) {
            this.setupStudioAudioChain();
            this.initAcousticWaveTables();
            this.createNoiseBuffer();
        }
    },

    /**
     * Chaîne Audio de Mastering Studio :
     * VoiceBus -> Anti-Nasal Parametric EQ -> Warmth LowShelf -> Smooth HighShelf
     *          -> Master Compressor -> Split Dry/Wet (Convolver Reverb) -> MasterGain -> Analyser -> Destination
     */
    setupStudioAudioChain() {
        const ctx = this.ctx;

        // 1. Bus de mixage d'entrée pour toutes les voix
        this.voiceBus = ctx.createGain();
        this.voiceBus.gain.value = 1.0;

        // 2. Filtre Anti-Nasillard (Cut chirurgical à 1750 Hz, bande critique où se concentre le son nasillard/boîte)
        this.antiNasalEQ = ctx.createBiquadFilter();
        this.antiNasalEQ.type = 'peaking';
        this.antiNasalEQ.frequency.value = 1750;
        this.antiNasalEQ.Q.value = 1.3;
        this.antiNasalEQ.gain.value = -5.0; // Réduit le côté criard/nasillard

        // 3. Filtre de Chaleur Acoustique (Boost rond et soyeux dans les graves / bas médiums)
        this.warmthEQ = ctx.createBiquadFilter();
        this.warmthEQ.type = 'lowshelf';
        this.warmthEQ.frequency.value = 180;
        this.warmthEQ.gain.value = 3.2; // Ajoute du corps et de la rondeur de table d'harmonie

        // 4. Filtre d'Adoucissement des Aigus (Élimine le côté piquant numérique)
        this.smoothAirEQ = ctx.createBiquadFilter();
        this.smoothAirEQ.type = 'highshelf';
        this.smoothAirEQ.frequency.value = 5200;
        this.smoothAirEQ.gain.value = -2.5;

        // 5. Compresseur de Studio (Lie harmonieusement la polyphonie et évite toute distorsion)
        this.masterCompressor = ctx.createDynamicsCompressor();
        this.masterCompressor.threshold.value = -16;
        this.masterCompressor.knee.value = 20;
        this.masterCompressor.ratio.value = 2.8;
        this.masterCompressor.attack.value = 0.005;
        this.masterCompressor.release.value = 0.16;

        // 6. Réverbération Stéréo d'Auditorium / Salle de Concert (Impulse Response algorithmique)
        this.reverbNode = ctx.createConvolver();
        this.reverbNode.buffer = this.generateHallImpulse(1.6, 2.4);

        // Mixage Dry / Wet
        this.dryGain = ctx.createGain();
        this.dryGain.gain.value = 0.78; // Signal direct clair

        this.wetGain = ctx.createGain();
        this.wetGain.gain.value = 0.28; // Réverbération naturelle chaleureuse

        // 7. Contrôle de Volume Principal & Analyseur FFT
        this.masterGain = ctx.createGain();
        this.masterGain.gain.setValueAtTime(this.isMuted ? 0 : this.volume, ctx.currentTime);

        this.analyser = ctx.createAnalyser();
        this.analyser.fftSize = 64;
        this.analyser.smoothingTimeConstant = 0.8;

        // Connexions de la chaîne de traitement
        this.voiceBus.connect(this.antiNasalEQ);
        this.antiNasalEQ.connect(this.warmthEQ);
        this.warmthEQ.connect(this.smoothAirEQ);
        this.smoothAirEQ.connect(this.masterCompressor);

        // Sortie du compresseur vers Dry et Wet
        this.masterCompressor.connect(this.dryGain);
        this.masterCompressor.connect(this.reverbNode);
        this.reverbNode.connect(this.wetGain);

        this.dryGain.connect(this.masterGain);
        this.wetGain.connect(this.masterGain);

        this.masterGain.connect(this.analyser);
        this.analyser.connect(ctx.destination);
    },

    /**
     * Génère une réponse impulsionnelle de salle de concert feutrée (Concert Hall Impulse)
     * Utilise un bruit stéréo décorrélé avec atténuation exponentielle et filtre passe-bas chaleureux.
     */
    generateHallImpulse(duration, decay) {
        const rate = this.ctx.sampleRate;
        const length = Math.floor(rate * duration);
        const impulse = this.ctx.createBuffer(2, length, rate);
        const left = impulse.getChannelData(0);
        const right = impulse.getChannelData(1);

        let lastL = 0, lastR = 0;
        const damping = 0.84; // Amortissement doux simulant les boiseries et tentures de scène

        for (let i = 0; i < length; i++) {
            const t = i / length;
            const env = Math.pow(1 - t, decay);
            const rawL = (Math.random() * 2 - 1) * env;
            const rawR = (Math.random() * 2 - 1) * env;

            lastL = lastL * damping + rawL * (1 - damping);
            lastR = lastR * damping + rawR * (1 - damping);

            left[i] = lastL;
            right[i] = lastR;
        }
        return impulse;
    },

    /**
     * Initialise des tables d'ondes harmoniques (Fourier PeriodicWave)
     * Remplacent avantageusement les oscillateurs élémentaires (saw/square/triangle)
     * en éliminant les harmoniques métalliques agressives au profit d'harmoniques organiques.
     */
    initAcousticWaveTables() {
        const ctx = this.ctx;

        // 1. Table d'onde Piano de Concert (Décroissance naturelle riche en fondamentale et 2e/3e harmonique)
        const pianoHarmonics = [0, 1.0, 0.48, 0.22, 0.11, 0.05, 0.022, 0.009, 0.004];
        const pImag = new Float32Array(pianoHarmonics);
        const pReal = new Float32Array(pianoHarmonics.length);
        this.pianoWave = ctx.createPeriodicWave(pReal, pImag);

        // 2. Table d'onde Cordes / Violoncelles Soie (Harmoniques douces, sans le grincement de scie pure)
        const stringsHarmonics = [0, 0.9, 0.72, 0.54, 0.38, 0.24, 0.15, 0.08, 0.04, 0.02];
        const sImag = new Float32Array(stringsHarmonics);
        const sReal = new Float32Array(stringsHarmonics.length);
        this.stringsWave = ctx.createPeriodicWave(sReal, sImag);

        // 3. Table d'onde Basse Ronde (Fondamentale puissante et bas médium velouté)
        const bassHarmonics = [0, 1.0, 0.65, 0.25, 0.08, 0.02];
        const bImag = new Float32Array(bassHarmonics);
        const bReal = new Float32Array(bassHarmonics.length);
        this.bassWave = ctx.createPeriodicWave(bReal, bImag);

        // 4. Table d'onde Cuivres & Leads Chaleureux
        const brassHarmonics = [0, 1.0, 0.55, 0.35, 0.22, 0.14, 0.08, 0.03];
        const brImag = new Float32Array(brassHarmonics);
        const brReal = new Float32Array(brassHarmonics.length);
        this.brassWave = ctx.createPeriodicWave(brReal, brImag);
    },

    createNoiseBuffer() {
        if (!this.ctx) return;
        const bufferSize = this.ctx.sampleRate * 1.5;
        this.noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const output = this.noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }
    },

    setMuted(muted) {
        this.isMuted = muted;
        if (this.masterGain && this.ctx) {
            this.masterGain.gain.setValueAtTime(muted ? 0 : this.volume, this.ctx.currentTime);
        }
    },

    setVolume(vol) {
        this.volume = Math.max(0, Math.min(1, vol));
        if (this.masterGain && this.ctx && !this.isMuted) {
            this.masterGain.gain.setValueAtTime(this.volume, this.ctx.currentTime);
        }
    },

    loadTrack(track) {
        this.stop();
        this.currentTrack = track;
        this.duration = (track && track.duration) ? track.duration : 45;
        this.pauseOffset = 0;
        this.nextNoteIndex = 0;
    },

    play(track) {
        this.init();
        if (!this.ctx) return;

        if (track && track !== this.currentTrack) {
            this.loadTrack(track);
        }
        if (!this.currentTrack || !this.currentTrack.notes) return;

        this.isPlaying = true;
        this.startTime = this.ctx.currentTime - this.pauseOffset;

        this.nextNoteIndex = 0;
        const notes = this.currentTrack.notes;
        while (this.nextNoteIndex < notes.length && notes[this.nextNoteIndex][0] < this.pauseOffset) {
            this.nextNoteIndex++;
        }

        this.startScheduler();

        if (this.onPlayStateChange) {
            this.onPlayStateChange(true);
        }
    },

    pause() {
        if (!this.isPlaying) return;
        this.isPlaying = false;
        if (this.ctx) {
            this.pauseOffset = this.ctx.currentTime - this.startTime;
        }
        this.stopActiveVoices();
        this.stopScheduler();

        if (this.onPlayStateChange) {
            this.onPlayStateChange(false);
        }
    },

    togglePlay(track) {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play(track);
        }
    },

    stop() {
        this.isPlaying = false;
        this.pauseOffset = 0;
        this.nextNoteIndex = 0;
        this.stopActiveVoices();
        this.stopScheduler();

        if (this.onPlayStateChange) {
            this.onPlayStateChange(false);
        }
        if (this.onTimeUpdate) {
            this.onTimeUpdate(0, this.duration);
        }
    },

    seek(seconds) {
        const wasPlaying = this.isPlaying;
        this.stop();
        this.pauseOffset = Math.max(0, Math.min(seconds, this.duration));
        if (wasPlaying) {
            this.play();
        } else if (this.onTimeUpdate) {
            this.onTimeUpdate(this.pauseOffset, this.duration);
        }
    },

    startScheduler() {
        this.stopScheduler();
        const lookaheadMs = 70;
        const scheduleAheadTime = 0.35;

        this.schedulerInterval = setInterval(() => {
            if (!this.isPlaying || !this.ctx || !this.currentTrack) return;

            const currentTime = this.ctx.currentTime;
            const currentSongTime = currentTime - this.startTime;

            if (this.onTimeUpdate) {
                this.onTimeUpdate(Math.min(currentSongTime, this.duration), this.duration);
            }

            if (currentSongTime >= this.duration) {
                this.stop();
                if (this.onTrackEnd) this.onTrackEnd();
                return;
            }

            const notes = this.currentTrack.notes;
            const maxScheduleTime = currentSongTime + scheduleAheadTime;

            while (this.nextNoteIndex < notes.length) {
                const noteData = notes[this.nextNoteIndex];
                const noteTime = noteData[0];

                if (noteTime <= maxScheduleTime) {
                    if (noteTime >= currentSongTime - 0.05) {
                        const scheduleWhen = this.startTime + noteTime;
                        this.playNote(noteData, Math.max(this.ctx.currentTime, scheduleWhen));
                    }
                    this.nextNoteIndex++;
                } else {
                    break;
                }
            }
        }, lookaheadMs);
    },

    stopScheduler() {
        if (this.schedulerInterval) {
            clearInterval(this.schedulerInterval);
            this.schedulerInterval = null;
        }
    },

    stopActiveVoices() {
        for (let i = 0; i < this.activeVoices.length; i++) {
            const v = this.activeVoices[i];
            try {
                if (v.stop) v.stop();
                if (v.disconnect) v.disconnect();
            } catch (e) {}
        }
        this.activeVoices = [];
    },

    /**
     * Dispatch et synthèse des notes MIDI
     */
    playNote(noteData, when) {
        if (!this.ctx || !this.voiceBus) return;

        const pitch = noteData[1];
        const dur = Math.max(0.05, noteData[2]);
        const vel = Math.max(20, Math.min(127, noteData[3])) / 127;
        const channel = noteData[4];
        const program = noteData[5] || 0;

        // Canal 9 = Percussions General MIDI
        if (channel === 9) {
            this.playAcousticDrum(pitch, vel, when);
            return;
        }

        const freq = 440 * Math.pow(2, (pitch - 69) / 12);
        if (freq < 20 || freq > 14000) return;

        if (program >= 40 && program <= 51) {
            // Cordes / Violons / Orchestre
            this.synthesizeRichStrings(freq, dur, vel, when);
        } else if (program >= 32 && program <= 39) {
            // Basse acoustique / électrique
            this.synthesizeDeepBass(freq, dur, vel, when);
        } else if (program >= 56 && program <= 71) {
            // Cuivres & Cors
            this.synthesizeWarmBrass(freq, dur, vel, when);
        } else if (program >= 80 && program <= 95) {
            // Synthétiseurs & Leads
            this.synthesizeSmoothLead(freq, dur, vel, when);
        } else {
            // Piano de Concert Acoustique
            this.synthesizeConcertPiano(freq, dur, vel, when);
        }
    },

    /**
     * PIANO DE CONCERT ACOUSTIQUE
     * - Double oscillateur PeriodicWave légèrement désaccordé (±1.6 cents) simulant le trichorde de cordes
     * - Micro-impact d'attaque imitant le coup de marteau feutré sur la corde
     * - Enveloppe dynamique de filtre passe-bas : extinction rapide des aigus et résonance chaleureuse des graves
     */
    synthesizeConcertPiano(freq, dur, vel, when) {
        const ctx = this.ctx;

        // 1. Corde principale
        const osc1 = ctx.createOscillator();
        if (this.pianoWave) osc1.setPeriodicWave(this.pianoWave);
        else osc1.type = 'triangle';
        osc1.frequency.setValueAtTime(freq * Math.pow(2, 1.6 / 1200), when); // +1.6 cents

        // 2. Corde secondaire (effet de chœur naturel d'un piano acoustique)
        const osc2 = ctx.createOscillator();
        if (this.pianoWave) osc2.setPeriodicWave(this.pianoWave);
        else osc2.type = 'sine';
        osc2.frequency.setValueAtTime(freq * Math.pow(2, -1.6 / 1200), when); // -1.6 cents

        // Filtre dynamique : l'attaque a de la brillance sans agressivité, puis s'arrondit
        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        const startCutoff = Math.min(3600, freq * (2.0 + vel * 1.5));
        const endCutoff = Math.max(140, freq * 0.9);
        filter.frequency.setValueAtTime(startCutoff, when);
        filter.frequency.exponentialRampToValueAtTime(endCutoff, when + Math.min(dur, 2.5));

        // Enveloppe d'amplitude (Attaque douce 7ms pour éviter le clic + décroissance exponentielle)
        const gain = ctx.createGain();
        const noteGain = vel * 0.20;
        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.linearRampToValueAtTime(noteGain, when + 0.007);
        const decayTime = Math.min(dur + 0.1, 3.2);
        gain.gain.exponentialRampToValueAtTime(0.0001, when + decayTime);

        // 3. Petit impact de marteau feutré (attaque physique réaliste)
        if (this.noiseBuffer && vel > 0.3) {
            const hammer = ctx.createBufferSource();
            hammer.buffer = this.noiseBuffer;
            const hammerFilter = ctx.createBiquadFilter();
            hammerFilter.type = 'bandpass';
            hammerFilter.frequency.setValueAtTime(320, when);
            hammerFilter.Q.setValueAtTime(2.0, when);

            const hammerGain = ctx.createGain();
            hammerGain.gain.setValueAtTime(vel * 0.05, when);
            hammerGain.gain.exponentialRampToValueAtTime(0.0001, when + 0.015);

            hammer.connect(hammerFilter);
            hammerFilter.connect(hammerGain);
            hammerGain.connect(this.voiceBus);

            hammer.start(when);
            hammer.stop(when + 0.02);
            this.activeVoices.push(hammer);
        }

        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(gain);
        gain.connect(this.voiceBus);

        osc1.start(when);
        osc2.start(when);
        const stopTime = when + decayTime;
        osc1.stop(stopTime);
        osc2.stop(stopTime);

        this.activeVoices.push(osc1, osc2);
    },

    /**
     * SECTION DE CORDES ORCHESTRALES SOYEUSES
     * - Double table d'ondes avec désaccordage de pupitre (±4 cents)
     * - LFO de vibrato expressif (5.2 Hz)
     * - Filtrage passe-bas velouté éliminant tout sifflement
     */
    synthesizeRichStrings(freq, dur, vel, when) {
        const ctx = this.ctx;

        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        if (this.stringsWave) {
            osc1.setPeriodicWave(this.stringsWave);
            osc2.setPeriodicWave(this.stringsWave);
        } else {
            osc1.type = 'sawtooth';
            osc2.type = 'sawtooth';
        }

        osc1.frequency.setValueAtTime(freq * Math.pow(2, 4.0 / 1200), when);
        osc2.frequency.setValueAtTime(freq * Math.pow(2, -4.0 / 1200), when);

        // LFO de vibrato subtil
        const lfo = ctx.createOscillator();
        const lfoGain = ctx.createGain();
        lfo.frequency.setValueAtTime(5.2, when);
        lfoGain.gain.setValueAtTime(freq * 0.006, when); // 0.6% de vibrato expressif
        lfo.connect(lfoGain);
        lfoGain.connect(osc1.frequency);
        lfoGain.connect(osc2.frequency);
        lfo.start(when + 0.1);
        lfo.stop(when + dur + 0.2);

        // Filtre soyeux à coupure basse (max 1400 Hz)
        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(Math.min(1400, Math.max(350, freq * 2.2)), when);

        const gain = ctx.createGain();
        const noteGain = vel * 0.13;
        const attack = 0.08;
        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.linearRampToValueAtTime(noteGain, when + attack);
        gain.gain.setValueAtTime(noteGain * 0.9, when + dur - 0.03);
        gain.gain.exponentialRampToValueAtTime(0.0001, when + dur + 0.22);

        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(gain);
        gain.connect(this.voiceBus);

        const stopTime = when + dur + 0.22;
        osc1.start(when);
        osc2.start(when);
        osc1.stop(stopTime);
        osc2.stop(stopTime);

        this.activeVoices.push(osc1, osc2, lfo);
    },

    /**
     * BASSE RONDE & CHALEUREUSE
     * - Double oscillateur (sub-fondamentale + harmonique)
     * - Filtre résonant centré sur la rondeur (380 Hz)
     */
    synthesizeDeepBass(freq, dur, vel, when) {
        const ctx = this.ctx;

        const oscSub = ctx.createOscillator();
        oscSub.type = 'sine';
        oscSub.frequency.setValueAtTime(freq, when);

        const oscBody = ctx.createOscillator();
        if (this.bassWave) oscBody.setPeriodicWave(this.bassWave);
        else oscBody.type = 'triangle';
        oscBody.frequency.setValueAtTime(freq, when);

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(420, when);
        filter.Q.setValueAtTime(1.5, when);

        const gain = ctx.createGain();
        const noteGain = vel * 0.26;
        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.linearRampToValueAtTime(noteGain, when + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.0001, when + Math.min(dur, 2.0));

        oscSub.connect(filter);
        oscBody.connect(filter);
        filter.connect(gain);
        gain.connect(this.voiceBus);

        const stopTime = when + Math.min(dur, 2.0);
        oscSub.start(when);
        oscBody.start(when);
        oscSub.stop(stopTime);
        oscBody.stop(stopTime);

        this.activeVoices.push(oscSub, oscBody);
    },

    /**
     * CUIVRES & CORS DOUX
     */
    synthesizeWarmBrass(freq, dur, vel, when) {
        const ctx = this.ctx;

        const osc = ctx.createOscillator();
        if (this.brassWave) osc.setPeriodicWave(this.brassWave);
        else osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, when);

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        // Ouverture de filtre progressive imitant le souffle du cuivre
        filter.frequency.setValueAtTime(Math.min(900, freq * 1.5), when);
        filter.frequency.exponentialRampToValueAtTime(Math.min(2200, freq * 2.8), when + 0.08);

        const gain = ctx.createGain();
        const noteGain = vel * 0.15;
        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.linearRampToValueAtTime(noteGain, when + 0.04);
        gain.gain.setValueAtTime(noteGain * 0.85, when + dur - 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, when + dur + 0.1);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.voiceBus);

        const stopTime = when + dur + 0.1;
        osc.start(when);
        osc.stop(stopTime);

        this.activeVoices.push(osc);
    },

    /**
     * SYNTH LEAD / NEW WAVE VELOUTÉ
     */
    synthesizeSmoothLead(freq, dur, vel, when) {
        const ctx = this.ctx;

        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        osc1.type = 'sawtooth';
        osc2.type = 'triangle';
        osc1.frequency.setValueAtTime(freq, when);
        osc2.frequency.setValueAtTime(freq * Math.pow(2, 2.5 / 1200), when); // Détuning fin

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(Math.min(2400, freq * 2.6), when);

        const gain = ctx.createGain();
        const noteGain = vel * 0.12;
        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.linearRampToValueAtTime(noteGain, when + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.0001, when + dur + 0.06);

        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(gain);
        gain.connect(this.voiceBus);

        const stopTime = when + dur + 0.06;
        osc1.start(when);
        osc2.start(when);
        osc1.stop(stopTime);
        osc2.stop(stopTime);

        this.activeVoices.push(osc1, osc2);
    },

    /**
     * BATTERIE ACOUSTIQUE NATURELLE
     */
    playAcousticDrum(pitch, vel, when) {
        if (!this.ctx || !this.voiceBus) return;
        const ctx = this.ctx;

        // Grosse Caisse (Kick 35, 36) - Punch dynamique et sub-bass rond
        if (pitch === 35 || pitch === 36) {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(130, when);
            osc.frequency.exponentialRampToValueAtTime(42, when + 0.09);

            gain.gain.setValueAtTime(vel * 0.32, when);
            gain.gain.exponentialRampToValueAtTime(0.001, when + 0.16);

            osc.connect(gain);
            gain.connect(this.voiceBus);

            osc.start(when);
            osc.stop(when + 0.16);
            this.activeVoices.push(osc);
        }
        // Caisse Claire (Snare 38, 40) - Fût en bois (185 Hz) + timbre en bruit blanc feutré
        else if (pitch === 38 || pitch === 40) {
            // Corps de fût
            const osc = ctx.createOscillator();
            const oscGain = ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(185, when);
            osc.frequency.exponentialRampToValueAtTime(80, when + 0.08);
            oscGain.gain.setValueAtTime(vel * 0.16, when);
            oscGain.gain.exponentialRampToValueAtTime(0.001, when + 0.09);
            osc.connect(oscGain);
            oscGain.connect(this.voiceBus);
            osc.start(when);
            osc.stop(when + 0.09);

            // Bruit de timbre
            if (this.noiseBuffer) {
                const noise = ctx.createBufferSource();
                noise.buffer = this.noiseBuffer;
                const filter = ctx.createBiquadFilter();
                filter.type = 'bandpass';
                filter.frequency.setValueAtTime(1600, when);
                filter.Q.setValueAtTime(1.1, when);

                const gain = ctx.createGain();
                gain.gain.setValueAtTime(vel * 0.15, when);
                gain.gain.exponentialRampToValueAtTime(0.001, when + 0.14);

                noise.connect(filter);
                filter.connect(gain);
                gain.connect(this.voiceBus);

                noise.start(when);
                noise.stop(when + 0.14);
                this.activeVoices.push(osc, noise);
            }
        }
        // Charleys / Cymbales (42, 44, 46, 49, 51) - Ciselé soyeux sans agressivité
        else if (pitch >= 42 && pitch <= 53) {
            if (this.noiseBuffer) {
                const noise = ctx.createBufferSource();
                noise.buffer = this.noiseBuffer;
                const filter = ctx.createBiquadFilter();
                filter.type = 'highpass';
                filter.frequency.setValueAtTime(6800, when);

                const gain = ctx.createGain();
                const decay = (pitch === 49 || pitch === 51) ? 0.38 : 0.045;
                gain.gain.setValueAtTime(vel * 0.07, when);
                gain.gain.exponentialRampToValueAtTime(0.001, when + decay);

                noise.connect(filter);
                filter.connect(gain);
                gain.connect(this.voiceBus);

                noise.start(when);
                noise.stop(when + decay);
                this.activeVoices.push(noise);
            }
        }
    },

    getFrequencyData(array) {
        if (!this.analyser || !this.isPlaying) {
            if (array) array.fill(0);
            return array;
        }
        this.analyser.getByteFrequencyData(array);
        return array;
    }
};

window.SoundEngine = SoundEngine;
window.MusicPlayer = MusicPlayer;
