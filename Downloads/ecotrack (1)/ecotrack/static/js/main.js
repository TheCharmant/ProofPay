// EcoTrack — main.js
document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash messages after 4s
    document.querySelectorAll('.flash').forEach(el => {
        setTimeout(() => el.remove(), 4000);
    });
});
