document.addEventListener('DOMContentLoaded', function () {

    // Fermer les résultats de recherche en cliquant ailleurs
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (searchInput && searchResults) {
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.innerHTML = '';
            }
        });

        // Fermer avec Escape
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                searchResults.innerHTML = '';
                searchInput.blur();
            }
        });

        // Vider les résultats si le champ est vide
        searchInput.addEventListener('input', function () {
            if (this.value.trim() === '') {
                searchResults.innerHTML = '';
            }
        });
    }

    // Animation d'apparition des cartes d'articles
    const cards = document.querySelectorAll('.article-card, .comment');
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(function (card) {
        card.classList.add('fade-target');
        observer.observe(card);
    });

    // Raccourci clavier : "/" pour focus sur la recherche
    document.addEventListener('keydown', function (e) {
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (searchInput) searchInput.focus();
        }
    });
});
