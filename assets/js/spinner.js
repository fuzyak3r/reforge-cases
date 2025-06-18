// Global variables for spinner
let spinnerItems = [];
let spinnerWonItem = null;
let spinnerWonIndex = 0;
let spinnerWonFloat = 0;
let isSpinning = false;

// Initialize the spinner with items
function initSpinner(items, wonIndex, wonItem) {
    spinnerItems = items;
    spinnerWonItem = wonItem;
    spinnerWonIndex = wonIndex;
    spinnerWonFloat = items[wonIndex].float || Math.random().toFixed(6);
    
    // Create spinner items HTML
    let itemsHtml = '';
    items.forEach(item => {
        let itemName = '';
        if (item.stattrak) {
            itemName += 'StatTrak™ ';
        } else if (item.souvenir) {
            itemName += 'Souvenir ';
        }
        itemName += `${item.weapon.title} | ${item.pattern.title}`;
        
        itemsHtml += `
            <div class="spinner-item">
                <div class="spinner-item-image-wrap">
                    <img src="${item.image}" alt="${itemName}" class="spinner-item-image">
                </div>
                <div class="spinner-item-title" style="background-color: ${item.quality.color}">
                    <strong>${item.weapon.title}</strong><br>${item.pattern.title}
                </div>
            </div>
        `;
    });
    
    // Add items to spinner
    $('#spinner-items').html(itemsHtml);
    
    // Start spinning animation
    setTimeout(startSpin, 500);
}

// Start the spinning animation
function startSpin() {
    isSpinning = true;
    
    // Calculate the distance to spin
    const itemWidth = 120; // Width of each item including margin
    const containerWidth = $('#spinner-roulette').width();
    const spinToIndex = spinnerWonIndex;
    
    // Calculate the position to move to (center the won item)
    const centerOffset = (containerWidth / 2) - (itemWidth / 2);
    const spinDistance = (spinToIndex * itemWidth) - centerOffset;
    
    // Add a random offset to make it less predictable
    const randomOffset = Math.floor(Math.random() * (itemWidth * 0.6));
    const finalDistance = spinDistance + randomOffset;
    
    // Apply the transform with animation
    $('#spinner-items').css({
        'transition': 'none',
        'transform': 'translateX(0)'
    });
    
    // Force a reflow
    $('#spinner-items')[0].offsetHeight;
    
    // Apply the animation
    $('#spinner-items').css({
        'transition': 'transform 5s cubic-bezier(0.215, 0.61, 0.355, 1)',
        'transform': `translateX(-${finalDistance}px)`
    });
    
    // When animation ends
    setTimeout(function() {
        isSpinning = false;
        showWonItem(spinnerWonItem, spinnerWonFloat);
    }, 5500);
}