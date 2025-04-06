console.log('Initialisation du mode sombre');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded - Début du script');
    
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) {
        console.error('ERREUR: Bouton darkModeToggle non trouvé');
        return;
    }

    const body = document.body;
    console.log('Éléments DOM trouvés');

    // Vérifier l'état initial
    const darkModeEnabled = localStorage.getItem('darkMode') === 'enabled';
    console.log('État initial du mode sombre:', darkModeEnabled);

    // Appliquer l'état initial
    if (darkModeEnabled) {
        body.classList.add('dark-mode');
        console.log('Mode sombre activé au chargement');
    } else {
        body.classList.add('light-mode');
        console.log('Mode clair activé au chargement');
    }

    // Mettre à jour le texte du bouton
    function updateButtonText(isDark) {
        const icon = isDark ? 'sun' : 'moon';
        const text = isDark ? 'Mode Clair' : 'Mode Sombre';
        darkModeToggle.innerHTML = `<i class="fas fa-${icon}"></i> ${text}`;
    }
    updateButtonText(darkModeEnabled);

    // Gestion du clic
    darkModeToggle.addEventListener('click', function() {
        console.log('Bouton mode sombre/claire cliqué');
        
        // Basculement du mode
        const isNowDark = !body.classList.contains('dark-mode');
        body.classList.toggle('dark-mode', isNowDark);
        body.classList.toggle('light-mode', !isNowDark);
        
        // Sauvegarde de l'état
        localStorage.setItem('darkMode', isNowDark ? 'enabled' : 'disabled');
        console.log('Nouvel état du mode:', isNowDark ? 'sombre' : 'clair');
        
        // Mise à jour du bouton
        updateButtonText(isNowDark);
    });

    console.log('Initialisation du mode sombre terminée');
});