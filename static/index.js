const gallery = document.getElementById('image-gallery');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');

async function loadImages() {
    try {
        const response = await fetch('/api/images');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const images = await response.json();
        loadingElement.style.display = 'none';
        images.forEach(createImageElement);
    } catch (error) {
        console.error('Error:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
    }
}

function createImageElement(image) {
    const container = document.createElement('div');
    container.className = 'image-container';

    const img = document.createElement('img');
    img.src = `/images/${image.id}.jpg`;
    img.alt = image.title;
    img.loading = 'lazy';

    const caption = document.createElement('div');
    caption.className = 'image-caption';
    caption.textContent = image.title;

    container.appendChild(img);
    container.appendChild(caption);
    gallery.appendChild(container);

    img.onerror = () => {
        container.remove();
        console.error(`Failed to load image: ${image.id}`);
    };
}

loadImages();