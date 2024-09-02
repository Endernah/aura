document.addEventListener('DOMContentLoaded', () => {
    const screenWidth = window.screen.width;
    const screenHeight = window.screen.height;
    if (screenWidth < 600 || screenHeight < 600) {
        document.body.innerHTML = "Access to this website is not allowed on devices with screens smaller than 600x600.";
    }
    console.log(screenWidth + 'x' + screenHeight);
});