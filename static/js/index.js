document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('search-input');
    input.addEventListener('input', showSuggestions);
});

function showSuggestions() {
    const input = document.getElementById('search-input');
    const filter = input.value.toLowerCase();
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = '';
    if (filter) {
        fetch(`/api/search?q=${filter}`)
            .then(response => response.json())
            .then(results => {
                results.forEach(result => {
                    const div = document.createElement('div');
                    div.textContent = result;
                    div.onclick = () => {
                        input.value = result;
                        suggestions.innerHTML = '';
                        suggestions.style.display = 'none';
                    };
                    suggestions.appendChild(div);
                });
                suggestions.style.display = results.length ? 'block' : 'none';
            })
            .catch(error => console.error('Error fetching search results:', error));
    } else {
        suggestions.style.display = 'none';
    }
}