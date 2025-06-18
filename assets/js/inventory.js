// Global variables
let inventory = [];
let filteredInventory = [];
let currentPage = 1;
let itemsPerPage = 12;
let selectedItem = null;

// Check authentication status
function checkAuth() {
    fetch('/api/user')
        .then(response => {
            if (response.status === 401) {
                window.location.href = 'profile.html';
                return { authenticated: false };
            }
            return response.json();
        })
        .then(data => {
            if (data.error || !data.steam_id) {
                // Not logged in, redirect to profile page
                window.location.href = 'profile.html';
            } else {
                // Logged in
                $('#login-item').html(`<span class="nav-link">Balance: $${data.balance.toFixed(2)}</span>`);
                fetchInventory();
            }
        })
        .catch(error => {
            console.error('Auth check error:', error);
        });
}

// Fetch inventory from API
function fetchInventory() {
    $('#inventory-loading').show();
    $('#inventory-empty').hide();
    
    fetch('/api/inventory')
        .then(response => {
            if (response.status === 401) {
                window.location.href = 'profile.html';
                return [];
            }
            return response.json();
        })
        .then(data => {
            inventory = data;
            filteredInventory = data;
            updateInventoryStats();
            
            if (inventory.length === 0) {
                $('#inventory-loading').hide();
                $('#inventory-empty').show();
            } else {
                displayInventory();
            }
        })
        .catch(error => {
            console.error('Error fetching inventory:', error);
            $('#inventory-loading').hide();
            $('#inventory-container').html('<div class="col-12"><div class="alert alert-danger">Error loading inventory. Please try again later.</div></div>');
        });
}

// Update inventory statistics
function updateInventoryStats() {
    const totalValue = filteredInventory.reduce((sum, item) => sum + item.skin.price, 0);
    $('#inventory-count').text(filteredInventory.length);
    $('#inventory-value').text(totalValue.toFixed(2));
}

// Display inventory items with pagination
function displayInventory() {
    $('#inventory-loading').hide();
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedItems = filteredInventory.slice(startIndex, endIndex);
    
    let itemsHtml = '';
    
    paginatedItems.forEach(item => {
        // Determine border color based on StatTrak or quality
        let borderColor = item.skin.quality.color;
        if (item.skin.stattrak) {
            borderColor = 'rgb(207, 106, 50)';
        } else if (item.skin.souvenir) {
            borderColor = 'rgb(255, 215, 0)';
        }
        
        // Format item name
        let itemName = '';
        if (item.skin.stattrak) {
            itemName += 'StatTrak™ ';
        } else if (item.skin.souvenir) {
            itemName += 'Souvenir ';
        }
        itemName += `${item.skin.weapon.title} | ${item.skin.pattern.title}`;
        
        // Determine exterior name
        const exterior = getExteriorName(item.float);
        
        itemsHtml += `
            <div class="col-md-3 col-sm-6 mb-4">
                <div class="inventory-item-card" data-id="${item._id}" style="border-color: ${borderColor}">
                    <div class="inventory-item-image-wrap">
                        <img src="${item.skin.image}" alt="${itemName}" class="inventory-item-image">
                        <span class="inventory-item-float">${exterior} (${item.float.toFixed(4)})</span>
                    </div>
                    <div class="inventory-item-title" style="background-color: ${item.skin.quality.color}">
                        <div class="inventory-item-weapon">${itemName}</div>
                        <div class="inventory-item-price">$${item.skin.price.toFixed(2)}</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    $('#inventory-container').html(itemsHtml);
    
    // Create pagination
    updatePagination();
    
    // Add click event to items
    $('.inventory-item-card').click(function() {
        const itemId = $(this).data('id');
        showItemDetails(itemId);
    });
}

// Update pagination controls
function updatePagination() {
    const totalPages = Math.ceil(filteredInventory.length / itemsPerPage);
    
    if (totalPages <= 1) {
        $('#pagination-container').empty();
        return;
    }
    
    let paginationHtml = `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>
        </li>
    `;
    
    for (let i = 1; i <= totalPages; i++) {
        paginationHtml += `
            <li class="page-item ${currentPage === i ? 'active' : ''}">
                <a class="page-link" href="#" data-page="${i}">${i}</a>
            </li>
        `;
    }
    
    paginationHtml += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>
        </li>
    `;
    
    $('#pagination-container').html(paginationHtml);
    
    // Add click event to pagination links
    $('.page-link').click(function(e) {
        e.preventDefault();
        const page = parseInt($(this).data('page'));
        
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
            displayInventory();
        }
    });
}

// Show item details in modal
function showItemDetails(itemId) {
    selectedItem = inventory.find(item => item._id === itemId);
    
    if (selectedItem) {
        // Format item name
        let itemName = '';
        if (selectedItem.skin.stattrak) {
            itemName += 'StatTrak™ ';
        } else if (selectedItem.skin.souvenir) {
            itemName += 'Souvenir ';
        }
        itemName += `${selectedItem.skin.weapon.title} | ${selectedItem.skin.pattern.title}`;
        
        // Get exterior name
        const exterior = getExteriorName(selectedItem.float);
        
        // Calculate sell price (90% of market value)
        const sellPrice = (selectedItem.skin.price * 0.9).toFixed(2);
        
        // Set modal content
        $('#itemModalTitle').text(itemName).css('color', selectedItem.skin.quality.color);
        $('#item-modal-image').attr('src', selectedItem.skin.image);
        $('#item-modal-exterior').text(exterior);
        $('#item-modal-float').text(selectedItem.float.toFixed(6));
        $('#item-modal-quality').text(selectedItem.skin.quality.title).css('color', selectedItem.skin.quality.color);
        $('#item-modal-price').text(selectedItem.skin.price.toFixed(2));
        $('#item-sell-price').text(sellPrice);
        
        $('#itemModal').modal('show');
    }
}

// Sell item
function sellItem() {
    if (!selectedItem) return;
    
    fetch(`/api/sell-item/${selectedItem._id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Update displayed balance
        $('#login-item').html(`<span class="nav-link">Balance: $${data.new_balance.toFixed(2)}</span>`);
        
        // Remove item from inventory
        inventory = inventory.filter(item => item._id !== selectedItem._id);
        filteredInventory = filteredInventory.filter(item => item._id !== selectedItem._id);
        
        // Update display
        updateInventoryStats();
        
        if (filteredInventory.length === 0) {
            $('#inventory-empty').show();
            $('#pagination-container').empty();
        } else {
            // Adjust current page if needed
            const totalPages = Math.ceil(filteredInventory.length / itemsPerPage);
            if (currentPage > totalPages) {
                currentPage = totalPages;
            }
            displayInventory();
        }
        
        // Close modal
        $('#itemModal').modal('hide');
    })
    .catch(error => {
        console.error('Error selling item:', error);
        alert('Error selling item. Please try again.');
    });
}

// Search inventory items
function searchInventory(query) {
    if (!query) {
        filteredInventory = inventory;
    } else {
        query = query.toLowerCase();
        filteredInventory = inventory.filter(item => {
            let itemName = '';
            if (item.skin.stattrak) {
                itemName += 'StatTrak™ ';
            } else if (item.skin.souvenir) {
                itemName += 'Souvenir ';
            }
            itemName += `${item.skin.weapon.title} | ${item.skin.pattern.title}`;
            
            return itemName.toLowerCase().includes(query);
        });
    }
    
    // Reset to first page
    currentPage = 1;
    
    // Update display
    updateInventoryStats();
    
    if (filteredInventory.length === 0) {
        $('#inventory-container').empty();
        $('#inventory-empty').show().find('.alert').text(`No items found matching "${query}"`);
        $('#pagination-container').empty();
    } else {
        $('#inventory-empty').hide();
        displayInventory();
    }
}

// Helper: Get exterior name based on float value
function getExteriorName(float) {
    if (float < 0.07) return 'Factory New';
    if (float < 0.15) return 'Minimal Wear';
    if (float < 0.38) return 'Field-Tested';
    if (float < 0.45) return 'Well-Worn';
    return 'Battle-Scarred';
}

// Initialize page
$(document).ready(function() {
    checkAuth();
    
    // Search input event
    $('#inventory-search').on('input', function() {
        const query = $(this).val();
        searchInventory(query);
    });
    
    // Clear search button
    $('#clear-search').click(function() {
        $('#inventory-search').val('');
        searchInventory('');
    });
    
    // Sell item button
    $('#sell-item-btn').click(sellItem);
});