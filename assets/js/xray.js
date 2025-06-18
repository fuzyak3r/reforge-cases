// Scan the case to reveal item
function scanCase() {
    if (!selectedCase) return;
    
    // Check if user has enough balance for scanning
    if (userBalance < scanFee) {
        alert(`Недостаточно средств для сканирования. Необходимо: ${scanFee.toFixed(2)} RC`);
        return;
    }
    
    // Start scanning animation
    $('.xray-scan').addClass('active').css('opacity', '1');
    
    // Hide the case image and message
    $('.xray-content-hidden').css('opacity', '0.3');
    
    // Add scanning status text
    let scanningStatus = $('<div class="scanning-status">Сканирование...</div>');
    $('.xray-container').append(scanningStatus);
    scanningStatus.fadeIn();
    
    // Call the scan-case API endpoint
    fetch(`/api/scan-case/${selectedCase._id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            $('.xray-scan').removeClass('active').css('opacity', '0');
            $('.xray-content-hidden').css('opacity', '1');
            scanningStatus.fadeOut(function() {
                $(this).remove();
            });
            return;
        }
        
        // Update user balance
        userBalance = data.new_balance;
        $('#header-balance').text(userBalance.toFixed(2));
        
        // Store the won item for later use
        selectedItem = data.wonItem;
        
        // Wait for scan animation
        setTimeout(() => {
            // Show the revealed item
            $('#xray-item-img').attr('src', selectedItem.image);
            
            // Format item name with StatTrak or Souvenir if needed
            let itemName = '';
            if (selectedItem.stattrak) {
                itemName += '<span style="color: #CF6A32;">StatTrak™</span> ';
            } else if (selectedItem.souvenir) {
                itemName += '<span style="color: #FFD700;">Souvenir</span> ';
            }
            itemName += `${selectedItem.weapon.title} | ${selectedItem.pattern.title}`;
            
            // Set item name with quality color
            $('#xray-item-name').html(itemName).css('color', selectedItem.quality.color);
            
            // Hide the case image completely
            $('.xray-content-hidden').css('opacity', '0');
            
            // Hide scanning status
            scanningStatus.fadeOut(function() {
                $(this).remove();
            });
            
            // Show the revealed content with animation
            $('.xray-content-revealed').addClass('active');
            
            // Reduce scan animation opacity but keep it running for x-ray effect
            $('.xray-scan').css('opacity', '0.5');
            
            // Hide scan button, show open and discard buttons
            $('#scan-case-btn').hide();
            $('#open-scanned-case-btn').show();
            $('#discard-case-btn').show();
            
            // Update scan status
            isScanned = true;
        }, 2000);
    })
    .catch(error => {
        console.error('Error scanning case:', error);
        alert('Error scanning case. Please try again.');
        $('.xray-scan').removeClass('active').css('opacity', '0');
        $('.xray-content-hidden').css('opacity', '1');
        scanningStatus.fadeOut(function() {
            $(this).remove();
        });
    });
}