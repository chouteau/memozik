/**
 * MemoZik - Moteur de jeu interactif & Blind Test Musical
 * HTML5 / CSS3 / JavaScript Vanilla
 */

(function () {
    'use strict';

    // --- État Global de l'Application ---
    const AppState = {
        category: 'all',          // 'all', 'classical', 'pop_rock', 'soundtrack'
        questionCount: 20,        // 10, 20 ou 30 morceaux
        showClues: true,          // Affichage des indices
        currentIndex: 0,
        score: 0,
        sessionTracks: [],        // Les 20 morceaux tirés au sort
        currentOptions: [],       // Les 4 propositions actuelles
        correctOptionIndex: -1,
        isAnswered: false,
        sessionResults: [],       // Historique des réponses pour le bilan
        startTime: null,
        endTime: null,
        modalPlayingTrackId: null
    };

    // --- Sélecteurs DOM ---
    const DOM = {
        // En-tête & Préférences
        themeToggle: document.getElementById('btn-toggle-theme'),
        soundToggle: document.getElementById('btn-toggle-sound'),
        btnOpenMusicNav: document.getElementById('btn-open-musicotheque'),
        brandLogo: document.getElementById('brand-logo'),

        // Écrans
        screenSetup: document.getElementById('screen-setup'),
        screenQuiz: document.getElementById('screen-quiz'),
        screenBilan: document.getElementById('screen-bilan'),

        // Écran 1 : Setup
        selectCategory: document.getElementById('select-category'),
        selectCount: document.getElementById('select-count'),
        checkClues: document.getElementById('check-clues'),
        btnStartQuiz: document.getElementById('btn-start-quiz'),
        btnOpenMusicSetup: document.getElementById('btn-open-musicotheque-setup'),
        statGamesPlayed: document.getElementById('stat-games-played'),
        statBestScore: document.getElementById('stat-best-score'),
        statSuccessRate: document.getElementById('stat-success-rate'),

        // Écran 2 : Quiz En-tête
        quizProgressText: document.getElementById('quiz-progress-text'),
        quizScoreLive: document.getElementById('quiz-score-live'),
        quizProgressBar: document.getElementById('quiz-progress-bar'),

        // Écran 2 : Platine Vinyle & Lecteur
        clueTag: document.getElementById('clue-tag'),
        vinylDisc: document.getElementById('vinyl-disc'),
        tonearm: document.getElementById('tonearm'),
        equalizerBars: document.getElementById('equalizer-bars'),
        timeCurrent: document.getElementById('time-current'),
        timeTotal: document.getElementById('time-total'),
        timelineSlider: document.getElementById('timeline-slider'),
        btnPlayPause: document.getElementById('btn-play-pause'),
        playIcon: document.getElementById('play-icon'),
        playText: document.getElementById('play-text'),
        btnReplay: document.getElementById('btn-replay'),
        volumeSlider: document.getElementById('volume-slider'),

        // Écran 2 : QCM & Révélation
        optionsContainer: document.getElementById('options-container'),
        eduCard: document.getElementById('educational-card'),
        eduTitle: document.getElementById('edu-title'),
        eduComposer: document.getElementById('edu-composer'),
        eduBadge: document.getElementById('edu-badge'),
        eduGenre: document.getElementById('edu-genre'),
        eduInstrumentation: document.getElementById('edu-instrumentation'),
        eduEra: document.getElementById('edu-era'),
        eduCountry: document.getElementById('edu-country'),
        eduFunfactText: document.getElementById('edu-funfact-text'),
        btnNextQuestion: document.getElementById('btn-next-question'),

        // Écran 3 : Bilan
        bilanScoreRaw: document.getElementById('bilan-score-raw'),
        bilanScorePercent: document.getElementById('bilan-score-percent'),
        bilanTime: document.getElementById('bilan-time'),
        bilanRankBadge: document.getElementById('bilan-rank-badge'),
        bilanRankComment: document.getElementById('bilan-rank-comment'),
        bilanReviewList: document.getElementById('bilan-review-list'),
        btnRestartQuiz: document.getElementById('btn-restart-quiz'),
        btnOpenMusicBilan: document.getElementById('btn-open-musicotheque-bilan'),

        // Modale Musicothèque
        modalMusicotheque: document.getElementById('modal-musicotheque'),
        btnCloseModal: document.getElementById('btn-close-modal'),
        searchMusic: document.getElementById('search-music'),
        filterPills: document.querySelectorAll('.filter-pill'),
        musicothequeList: document.getElementById('musicotheque-list')
    };

    // Nombre de barres d'égaliseur
    const EQ_BAR_COUNT = 24;
    let eqBarElements = [];
    let freqDataArray = null;

    // --- Utilitaires ---
    function formatTime(seconds) {
        if (isNaN(seconds) || seconds < 0) seconds = 0;
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s < 10 ? '0' : ''}${s}`;
    }

    function shuffleArray(arr) {
        const copy = [...arr];
        for (let i = copy.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copy[i], copy[j]] = [copy[j], copy[i]];
        }
        return copy;
    }

    // =========================================================================
    // Initialisation de l'Application
    // =========================================================================
    function init() {
        initTheme();
        initSound();
        initEqualizerBars();
        initEventListeners();
        loadPlayerStats();
        setupMusicPlayerCallbacks();
    }

    // --- Gestion du Thème Sombre / Clair ---
    function initTheme() {
        const savedTheme = localStorage.getItem('memozik_theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('memozik_theme', next);
        updateThemeIcon(next);
        SoundEngine.playClick();
    }

    function updateThemeIcon(theme) {
        if (DOM.themeToggle) {
            DOM.themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
            DOM.themeToggle.title = theme === 'dark' ? 'Basculer en thème Clair' : 'Basculer en thème Sombre';
        }
    }

    // --- Gestion du Son & Mute ---
    function initSound() {
        const isMuted = SoundEngine.loadMuteState();
        updateSoundIcon(isMuted);
    }

    function toggleSound() {
        const muted = SoundEngine.toggleMute();
        updateSoundIcon(muted);
        if (!muted) SoundEngine.playClick();
    }

    function updateSoundIcon(muted) {
        if (DOM.soundToggle) {
            DOM.soundToggle.textContent = muted ? '🔇' : '🔊';
            DOM.soundToggle.title = muted ? 'Activer le son' : 'Couper le son';
        }
    }

    // --- Initialisation du Visualiseur Audio ---
    function initEqualizerBars() {
        if (!DOM.equalizerBars) return;
        DOM.equalizerBars.innerHTML = '';
        eqBarElements = [];
        for (let i = 0; i < EQ_BAR_COUNT; i++) {
            const bar = document.createElement('div');
            bar.className = 'eq-bar';
            DOM.equalizerBars.appendChild(bar);
            eqBarElements.push(bar);
        }
        freqDataArray = new Uint8Array(32);
        requestAnimationFrame(updateVisualizerLoop);
    }

    function updateVisualizerLoop() {
        if (MusicPlayer.isPlaying) {
            MusicPlayer.getFrequencyData(freqDataArray);
            for (let i = 0; i < eqBarElements.length; i++) {
                const val = freqDataArray[i] || 0;
                const heightPx = Math.max(4, Math.round((val / 255) * 36));
                eqBarElements[i].style.height = `${heightPx}px`;
            }
        } else {
            for (let i = 0; i < eqBarElements.length; i++) {
                eqBarElements[i].style.height = '4px';
            }
        }
        requestAnimationFrame(updateVisualizerLoop);
    }

    // --- Synchronisation du Lecteur de Musique avec l'UI ---
    function setupMusicPlayerCallbacks() {
        MusicPlayer.onPlayStateChange = function (isPlaying) {
            if (isPlaying) {
                DOM.vinylDisc.classList.add('spinning');
                DOM.tonearm.classList.add('playing');
                DOM.playIcon.textContent = '⏸';
                DOM.playText.textContent = 'Pause';
            } else {
                DOM.vinylDisc.classList.remove('spinning');
                DOM.tonearm.classList.remove('playing');
                DOM.playIcon.textContent = '▶';
                DOM.playText.textContent = 'Écouter';
            }
        };

        MusicPlayer.onTimeUpdate = function (currentTime, totalDuration) {
            DOM.timeCurrent.textContent = formatTime(currentTime);
            DOM.timeTotal.textContent = formatTime(totalDuration);
            DOM.timelineSlider.value = currentTime;
            DOM.timelineSlider.max = totalDuration;
        };

        MusicPlayer.onTrackEnd = function () {
            DOM.vinylDisc.classList.remove('spinning');
            DOM.tonearm.classList.remove('playing');
            DOM.playIcon.textContent = '▶';
            DOM.playText.textContent = 'Écouter';
        };
    }

    // =========================================================================
    // Gestion des Écrans & Navigation
    // =========================================================================
    function showScreen(screenId) {
        DOM.screenSetup.classList.add('hidden');
        DOM.screenQuiz.classList.add('hidden');
        DOM.screenBilan.classList.add('hidden');

        if (screenId === 'setup') {
            DOM.screenSetup.classList.remove('hidden');
            MusicPlayer.stop();
        } else if (screenId === 'quiz') {
            DOM.screenQuiz.classList.remove('hidden');
        } else if (screenId === 'bilan') {
            DOM.screenBilan.classList.remove('hidden');
            MusicPlayer.stop();
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // =========================================================================
    // Démarrage & Déroulement d'une Session de Jeu
    // =========================================================================
    function startSession() {
        SoundEngine.playClick();
        AppState.category = DOM.selectCategory.value;
        AppState.questionCount = parseInt(DOM.selectCount.value, 10) || 20;
        AppState.showClues = DOM.checkClues.checked;

        // Filtrer les morceaux disponibles
        let pool = typeof MUSIC_TRACKS !== 'undefined' ? MUSIC_TRACKS : [];
        if (AppState.category !== 'all') {
            pool = pool.filter(t => t.category === AppState.category);
        }

        if (pool.length === 0) {
            alert("Aucun morceau trouvé pour cette catégorie.");
            return;
        }

        // Mélanger et sélectionner le nombre de questions
        const shuffled = shuffleArray(pool);
        AppState.sessionTracks = shuffled.slice(0, Math.min(AppState.questionCount, shuffled.length));
        AppState.questionCount = AppState.sessionTracks.length;

        AppState.currentIndex = 0;
        AppState.score = 0;
        AppState.sessionResults = [];
        AppState.startTime = new Date();
        AppState.endTime = null;

        showScreen('quiz');
        loadQuestion(0);
    }

    function loadQuestion(index) {
        AppState.currentIndex = index;
        AppState.isAnswered = false;
        const track = AppState.sessionTracks[index];

        // 1. Mise à jour de la barre d'avancement
        DOM.quizProgressText.textContent = `Morceau ${index + 1} / ${AppState.questionCount}`;
        DOM.quizScoreLive.textContent = `Score : ${AppState.score}`;
        const pct = Math.round(((index) / AppState.questionCount) * 100);
        DOM.quizProgressBar.style.width = `${pct}%`;

        // 2. Affichage de l'indice
        if (AppState.showClues) {
            DOM.clueTag.textContent = `💡 Indice : ${track.categoryLabel} • ${track.era}`;
            DOM.clueTag.parentElement.classList.remove('hidden');
        } else {
            DOM.clueTag.parentElement.classList.add('hidden');
        }

        // 3. Masquer la fiche éducative et le bouton suivant
        DOM.eduCard.classList.add('hidden');
        DOM.btnNextQuestion.classList.add('hidden');

        // 4. Préparer les 4 propositions de réponses
        const correctChoice = {
            composer: track.composer,
            title: track.title,
            isCorrect: true
        };

        const distractors = (track.distractors || []).map(d => ({
            composer: d.composer,
            title: d.title,
            isCorrect: false
        }));

        // Compléter si besoin avec d'autres morceaux du catalogue
        while (distractors.length < 3) {
            const randomTrack = MUSIC_TRACKS[Math.floor(Math.random() * MUSIC_TRACKS.length)];
            if (randomTrack.id !== track.id && !distractors.some(d => d.title === randomTrack.title)) {
                distractors.push({
                    composer: randomTrack.composer,
                    title: randomTrack.title,
                    isCorrect: false
                });
            }
        }

        const choices = shuffleArray([correctChoice, ...distractors.slice(0, 3)]);
        AppState.currentOptions = choices;
        AppState.correctOptionIndex = choices.findIndex(c => c.isCorrect);

        // 5. Générer les 4 boutons de propositions
        DOM.optionsContainer.innerHTML = '';
        choices.forEach((choice, i) => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.setAttribute('data-index', i);
            btn.innerHTML = `
                <span class="option-key">${i + 1}</span>
                <div class="option-content">
                    <span class="option-title">${choice.title}</span>
                    <span class="option-composer">${choice.composer}</span>
                </div>
            `;
            btn.addEventListener('click', () => handleChoice(i));
            DOM.optionsContainer.appendChild(btn);
        });

        // 6. Charger le morceau dans le lecteur et lancer la lecture
        MusicPlayer.loadTrack(track);
        MusicPlayer.play();
    }

    function handleChoice(selectedIndex) {
        if (AppState.isAnswered) return;
        AppState.isAnswered = true;

        const currentTrack = AppState.sessionTracks[AppState.currentIndex];
        const isCorrect = (selectedIndex === AppState.correctOptionIndex);

        // Feedback Audio & Incrément Score
        if (isCorrect) {
            AppState.score++;
            SoundEngine.playCorrect();
        } else {
            SoundEngine.playWrong();
        }

        // Mettre à jour l'affichage du score en direct
        DOM.quizScoreLive.textContent = `Score : ${AppState.score}`;

        // Coloration des boutons
        const optionButtons = DOM.optionsContainer.querySelectorAll('.option-btn');
        optionButtons.forEach((btn, i) => {
            btn.disabled = true;
            if (i === AppState.correctOptionIndex) {
                btn.classList.add('correct');
            } else if (i === selectedIndex && !isCorrect) {
                btn.classList.add('wrong');
            }
        });

        // Remplir et révéler la fiche éducative
        DOM.eduTitle.textContent = currentTrack.title;
        DOM.eduComposer.textContent = currentTrack.composer;
        DOM.eduBadge.className = `badge-category ${currentTrack.category}`;
        DOM.eduBadge.textContent = currentTrack.categoryLabel;

        DOM.eduGenre.textContent = currentTrack.genre || '—';
        DOM.eduInstrumentation.textContent = currentTrack.instrumentation || '—';
        DOM.eduEra.textContent = `${currentTrack.era} (${currentTrack.year})`;
        DOM.eduCountry.textContent = currentTrack.country || '—';
        DOM.eduFunfactText.textContent = currentTrack.funFact || 'Aucune anecdote disponible.';

        DOM.eduCard.classList.remove('hidden');
        DOM.btnNextQuestion.classList.remove('hidden');

        // Enregistrer dans les résultats de session
        AppState.sessionResults.push({
            track: currentTrack,
            selectedIndex: selectedIndex,
            correctIndex: AppState.correctOptionIndex,
            isCorrect: isCorrect,
            chosenOption: AppState.currentOptions[selectedIndex]
        });
    }

    function nextQuestion() {
        SoundEngine.playClick();
        if (AppState.currentIndex + 1 < AppState.questionCount) {
            loadQuestion(AppState.currentIndex + 1);
        } else {
            showBilan();
        }
    }

    // =========================================================================
    // Écran 3 : Bilan de Fin de Session & Statistiques
    // =========================================================================
    function showBilan() {
        AppState.endTime = new Date();
        MusicPlayer.stop();

        const durationSeconds = Math.round((AppState.endTime - AppState.startTime) / 1000);
        const minutes = Math.floor(durationSeconds / 60);
        const seconds = durationSeconds % 60;
        const timeFormatted = `${minutes} min ${seconds < 10 ? '0' : ''}${seconds} s`;

        const total = AppState.questionCount;
        const score = AppState.score;
        const percent = Math.round((score / total) * 100);

        // Mise à jour des cartes métriques
        DOM.bilanScoreRaw.textContent = `${score} / ${total}`;
        DOM.bilanScorePercent.textContent = `${percent}%`;
        DOM.bilanTime.textContent = timeFormatted;

        // Calcul du rang et commentaire
        let rankClass = 'rank-novice';
        let rankTitle = '🎵 Apprenti Mélomane';
        let rankComment = "La musique n'attend que vous ! Explorez la Musicothèque pour enrichir votre culture musicale.";

        if (score === total) {
            rankClass = 'rank-virtuoso';
            rankTitle = '🏆 Virtuose Absolu';
            rankComment = 'Sans-faute légendaire ! Vous possédez une oreille absolue et une culture musicale digne des plus grands maestros.';
            SoundEngine.playFanfare();
        } else if (score >= total * 0.85) {
            rankClass = 'rank-maestro';
            rankTitle = '🎻 Mélomane Émérite';
            rankComment = 'Performance remarquable ! Vous reconnaissez les nuances subtiles et maîtrisez une vaste panoplie de répertoires.';
            SoundEngine.playFanfare();
        } else if (score >= total * 0.70) {
            rankClass = 'rank-passionate';
            rankTitle = '🎶 Musicien Passionné';
            rankComment = 'Très bon score ! Votre oreille est fine et vos connaissances musicales sont solides.';
        } else if (score >= total * 0.50) {
            rankClass = 'rank-amateur';
            rankTitle = '🎧 Amateur Averti';
            rankComment = 'Bonne oreille ! Avec un peu de pratique et de curiosité, vous atteindrez facilement les sommets.';
        }

        DOM.bilanRankBadge.className = `rank-badge ${rankClass}`;
        DOM.bilanRankBadge.textContent = rankTitle;
        DOM.bilanRankComment.textContent = rankComment;

        // Remplir le récapitulatif détaillé des 20 questions
        DOM.bilanReviewList.innerHTML = '';
        AppState.sessionResults.forEach((res, i) => {
            const item = document.createElement('div');
            item.className = 'review-item';
            item.innerHTML = `
                <div class="review-status">${res.isCorrect ? '✅' : '❌'}</div>
                <div class="review-meta">
                    <div class="review-title">${res.track.title}</div>
                    <div class="review-composer">${res.track.composer} (${res.track.year})</div>
                    ${!res.isCorrect ? `<small style="color:var(--wrong-text);font-size:0.8rem;">Votre réponse : ${res.chosenOption ? res.chosenOption.title : '—'}</small>` : ''}
                </div>
                <div class="review-actions">
                    <button class="btn-sm-play" title="Réécouter le morceau" data-track-id="${res.track.id}">▶</button>
                    <button class="btn-sm-info" title="Voir l'anecdote" data-track-id="${res.track.id}">Fiche</button>
                </div>
            `;

            // Bouton réécouter dans le bilan
            const playBtn = item.querySelector('.btn-sm-play');
            playBtn.addEventListener('click', () => {
                SoundEngine.init();
                MusicPlayer.stop();
                MusicPlayer.loadTrack(res.track);
                MusicPlayer.play();
            });

            // Bouton voir fiche
            const infoBtn = item.querySelector('.btn-sm-info');
            infoBtn.addEventListener('click', () => {
                openMusicDetailsModal(res.track);
            });

            DOM.bilanReviewList.appendChild(item);
        });

        // Sauvegarde des statistiques locales
        savePlayerStats(score, total);

        showScreen('bilan');
    }

    // --- Sauvegarde & Chargement des Statistiques ---
    function savePlayerStats(score, total) {
        try {
            let stats = JSON.parse(localStorage.getItem('memozik_stats') || '{}');
            stats.gamesPlayed = (stats.gamesPlayed || 0) + 1;
            stats.totalQuestions = (stats.totalQuestions || 0) + total;
            stats.totalCorrect = (stats.totalCorrect || 0) + score;

            const bestScore = stats.bestScore || 0;
            if (score > bestScore) {
                stats.bestScore = score;
                stats.bestTotal = total;
            }

            localStorage.setItem('memozik_stats', JSON.stringify(stats));
            loadPlayerStats();
        } catch (e) {}
    }

    function loadPlayerStats() {
        try {
            const stats = JSON.parse(localStorage.getItem('memozik_stats') || '{}');
            const games = stats.gamesPlayed || 0;
            const best = stats.bestScore !== undefined ? `${stats.bestScore} / ${stats.bestTotal || 20}` : '0 / 20';
            const rate = stats.totalQuestions ? `${Math.round((stats.totalCorrect / stats.totalQuestions) * 100)}%` : '0%';

            if (DOM.statGamesPlayed) DOM.statGamesPlayed.textContent = games;
            if (DOM.statBestScore) DOM.statBestScore.textContent = best;
            if (DOM.statSuccessRate) DOM.statSuccessRate.textContent = rate;
        } catch (e) {}
    }

    // =========================================================================
    // Modale Musicothèque (Encyclopédie des 60 morceaux)
    // =========================================================================
    function openMusicotheque() {
        SoundEngine.playClick();
        renderMusicothequeCards();
        DOM.modalMusicotheque.classList.remove('hidden');
    }

    function closeMusicotheque() {
        DOM.modalMusicotheque.classList.add('hidden');
        if (AppState.modalPlayingTrackId) {
            MusicPlayer.stop();
            AppState.modalPlayingTrackId = null;
        }
    }

    function renderMusicothequeCards() {
        const query = (DOM.searchMusic.value || '').toLowerCase().trim();
        const activeFilter = document.querySelector('.filter-pill.active')?.getAttribute('data-filter') || 'all';

        let list = typeof MUSIC_TRACKS !== 'undefined' ? MUSIC_TRACKS : [];

        if (activeFilter !== 'all') {
            list = list.filter(t => t.category === activeFilter);
        }

        if (query) {
            list = list.filter(t => 
                t.title.toLowerCase().includes(query) ||
                t.composer.toLowerCase().includes(query) ||
                (t.genre && t.genre.toLowerCase().includes(query)) ||
                (t.era && t.era.toLowerCase().includes(query)) ||
                (t.funFact && t.funFact.toLowerCase().includes(query)) ||
                t.year.toString().includes(query)
            );
        }

        DOM.musicothequeList.innerHTML = '';
        if (list.length === 0) {
            DOM.musicothequeList.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 3rem 1rem;">
                    Aucun morceau trouvé pour « ${query} ».
                </div>
            `;
            return;
        }

        list.forEach(t => {
            const card = document.createElement('div');
            card.className = 'music-card';
            card.innerHTML = `
                <div class="music-card-top">
                    <div>
                        <div class="music-card-title">${t.title}</div>
                        <div class="music-card-composer">${t.composer}</div>
                    </div>
                    <span class="badge-category ${t.category}">${t.categoryLabel.split(' ')[0]}</span>
                </div>
                <div class="music-card-tags">
                    <span class="music-tag">📅 ${t.year}</span>
                    <span class="music-tag">🏛️ ${t.era}</span>
                    <span class="music-tag">🎼 ${t.genre || 'Classique'}</span>
                </div>
                <div class="music-card-desc">
                    💡 <strong>Le saviez-vous ?</strong> ${t.funFact}
                </div>
                <div class="music-card-footer">
                    <small style="color:var(--text-muted);">${t.country || ''}</small>
                    <button class="btn-card-play" data-track-id="${t.id}">
                        <span>▶ Écouter</span>
                    </button>
                </div>
            `;

            const playBtn = card.querySelector('.btn-card-play');
            playBtn.addEventListener('click', () => {
                SoundEngine.init();
                if (AppState.modalPlayingTrackId === t.id && MusicPlayer.isPlaying) {
                    MusicPlayer.pause();
                    playBtn.innerHTML = '<span>▶ Écouter</span>';
                    AppState.modalPlayingTrackId = null;
                } else {
                    MusicPlayer.stop();
                    // Réinitialiser les autres boutons
                    DOM.musicothequeList.querySelectorAll('.btn-card-play').forEach(b => {
                        b.innerHTML = '<span>▶ Écouter</span>';
                    });
                    MusicPlayer.loadTrack(t);
                    MusicPlayer.play();
                    playBtn.innerHTML = '<span>⏸ Pause</span>';
                    AppState.modalPlayingTrackId = t.id;
                }
            });

            DOM.musicothequeList.appendChild(card);
        });
    }

    function openMusicDetailsModal(track) {
        openMusicotheque();
        if (DOM.searchMusic) {
            DOM.searchMusic.value = track.title;
            renderMusicothequeCards();
        }
    }

    // =========================================================================
    // Gestion des Événements & Raccourcis Clavier
    // =========================================================================
    function initEventListeners() {
        // Navigation & Paramètres
        DOM.brandLogo.addEventListener('click', (e) => {
            e.preventDefault();
            SoundEngine.playClick();
            showScreen('setup');
        });

        DOM.themeToggle.addEventListener('click', toggleTheme);
        DOM.soundToggle.addEventListener('click', toggleSound);

        DOM.btnOpenMusicNav.addEventListener('click', openMusicotheque);
        DOM.btnOpenMusicSetup.addEventListener('click', openMusicotheque);
        DOM.btnOpenMusicBilan.addEventListener('click', openMusicotheque);
        DOM.btnCloseModal.addEventListener('click', closeMusicotheque);

        // Modale Backdrop Click
        DOM.modalMusicotheque.addEventListener('click', (e) => {
            if (e.target === DOM.modalMusicotheque) closeMusicotheque();
        });

        // Recherche & Filtres dans la Musicothèque
        DOM.searchMusic.addEventListener('input', renderMusicothequeCards);
        DOM.filterPills.forEach(pill => {
            pill.addEventListener('click', () => {
                DOM.filterPills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                renderMusicothequeCards();
            });
        });

        // Écran 1 : Lancement du Quiz
        DOM.btnStartQuiz.addEventListener('click', startSession);

        // Écran 2 : Commandes Audio
        DOM.btnPlayPause.addEventListener('click', () => {
            SoundEngine.init();
            MusicPlayer.togglePlay();
        });

        DOM.btnReplay.addEventListener('click', () => {
            SoundEngine.init();
            MusicPlayer.seek(0);
            MusicPlayer.play();
        });

        DOM.timelineSlider.addEventListener('input', (e) => {
            const time = parseFloat(e.target.value);
            MusicPlayer.seek(time);
        });

        DOM.volumeSlider.addEventListener('input', (e) => {
            const vol = parseFloat(e.target.value);
            MusicPlayer.setVolume(vol);
        });

        DOM.btnNextQuestion.addEventListener('click', nextQuestion);

        // Écran 3 : Relance d'une partie
        DOM.btnRestartQuiz.addEventListener('click', startSession);

        // Raccourcis Clavier
        window.addEventListener('keydown', handleKeyNavigation);
    }

    function handleKeyNavigation(e) {
        // Ignorer si l'utilisateur tape dans la barre de recherche
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;

        // Échap pour fermer la modale
        if (e.key === 'Escape' && !DOM.modalMusicotheque.classList.contains('hidden')) {
            closeMusicotheque();
            return;
        }

        // Pendant le Quiz
        if (!DOM.screenQuiz.classList.contains('hidden')) {
            // Touche Espace : Play / Pause
            if (e.key === ' ' || e.code === 'Space') {
                e.preventDefault();
                SoundEngine.init();
                MusicPlayer.togglePlay();
                return;
            }

            // Touche R : Rejouer
            if (e.key === 'r' || e.key === 'R') {
                e.preventDefault();
                SoundEngine.init();
                MusicPlayer.seek(0);
                MusicPlayer.play();
                return;
            }

            // Touches 1, 2, 3, 4 : Sélection d'une proposition
            if (['1', '2', '3', '4'].includes(e.key) && !AppState.isAnswered) {
                const idx = parseInt(e.key, 10) - 1;
                handleChoice(idx);
                return;
            }

            // Entrée ou N : Morceau suivant
            if ((e.key === 'Enter' || e.key === 'n' || e.key === 'N') && AppState.isAnswered) {
                e.preventDefault();
                nextQuestion();
                return;
            }
        }
    }

    // Démarrage au chargement du DOM
    document.addEventListener('DOMContentLoaded', init);

})();
