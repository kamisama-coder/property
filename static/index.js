let debounceTimeout;
const kami = 3;

// Function to make the API call
async function apiFunction(input) {
    const params = new URLSearchParams({
        q: input.replace(/ /g, '+'),
        format: "json",
        addressdetails: 1,
        polygon_geojson: 0
    });

    const api = "https://nominatim.openstreetmap.org/search?";

    try {
        const response = await fetch(`${api}${params.toString()}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

// Function to dynamically populate suggestions
async function necessary(input) {
    const parent = $(".new");
    parent.empty(); // Clear previous results to avoid duplication

    const response = await apiFunction(input);

    if (response.length === 0) {
        parent.append('<p class="error">No results found. Try a different query.</p>');
        return;
    }

    for (let i = 0; i < response.length; i++) {
        const childDiv = $('<p>', { 
            class: 'child', 
            text: response[i].display_name, 
            role: 'option', 
            tabindex: 0 // Allows keyboard navigation
        });
        childDiv.attr("data-lat", response[i].lat);
        childDiv.attr("data-long", response[i].lon); 
        parent.append(childDiv);
    }
}

// Debounced input handler
$('#exampleInputEmail1').on('input', function() {
    clearTimeout(debounceTimeout);
    $('.child').remove(); // Clear existing suggestions
    $('.error').remove(); // Clear any error messages

    const inputValue = $(this).val().trim();
    if (inputValue.length > kami) {
        debounceTimeout = setTimeout(() => necessary(inputValue), 300); // 300ms debounce
    }
});

// Handle click on suggestion
$(document).on("click", ".child", function() {
    $('#see').val($(this).text());
    $('#exampleInputEmail1').val($(this).text());
    $('[name="long"]').val($(this).attr('data-long'));
    $('[name="latt"]').val($(this).attr('data-lat'));
});

// Handle hover functionality for better user experience
$(".form-control").on("click", function() {
    var elementId = $(this).attr('id');
    if (elementId === 'exampleInputEmail1') {
        $(this).addClass('active');
    } else {
        $('#exampleInputEmail1').removeClass('active');
    }
});

// Optional: Add keyboard navigation for accessibility
$(document).on("keydown", ".child", function(e) {
    if (e.key === "Enter") {
        $(this).trigger("click");
    }
});

// Optional: Show a loading spinner during the API call
async function necessaryWithLoader(input) {
    const parent = $(".new");
    parent.empty().append('<p class="loading">Loading...</p>'); // Add loading spinner

    const response = await apiFunction(input);
    parent.find('.loading').remove(); // Remove spinner after data loads

    if (response.length === 0) {
        parent.append('<p class="error">No results found. Try a different query.</p>');
        return;
    }

    for (let i = 0; i < response.length; i++) {
        const childDiv = $('<p>', { 
            class: 'child', 
            text: response[i].display_name, 
            role: 'option', 
            tabindex: 0 
        });
        childDiv.attr("data-lat", response[i].lat);
        childDiv.attr("data-long", response[i].lon); 
        parent.append(childDiv);
    }
}



// var kami =  3;

// async function apiFunction(input) {
//     const params = new URLSearchParams({
//         q: input.replace(/ /g, '+'),
//         format: "json",
//         addressdetails: 1,
//         polygon_geojson: 0
//     });

//     const api = "https://nominatim.openstreetmap.org/search?";

//     try {
//         const response = await fetch(`${api}${params.toString()}`);
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error('Error:', error);
//         return [];
//     }
// }

// async function necessary(input) {
//     const parent = $(".new");
//     const response = await apiFunction(input);

//     for (let i = 0; i < response.length; i++) {
//         const childDiv1 = $('<p>', { class: 'child', text: response[i].display_name });
//         childDiv1.attr("data-lat", response[i].lat);
//         childDiv1.attr("data-long", response[i].lon); 
//         parent.append(childDiv1);
//     }
    
// }

// $(".form-control").on("click", function() {
//     var elementId = $(this).attr('id');
//     if (elementId == 'exampleInputEmail1') {
//         $(this).addClass('active');
//     } else {
//         $('#exampleInputEmail1').removeClass('active');
//     }
// });

// $('#exampleInputEmail1').on('input', function() {
//     $('.child').remove();
//     if ($(this).val().replace(/ /g, '').length > kami) {
//         necessary($(this).val());
//     }
// });

// $(document).on("click", ".child", function() {
//     $('#see').val($(this).text());
//     $('#exampleInputEmail1').val($(this).text());
//     $('[name="long"]').val($(this).attr('data-long'));
//     $('[name="latt"]').val($(this).attr('data-lat'));
// });

  // var checkInterval = setInterval(() => {
        //     console.log('jesus')
        //     if ($('#exampleInputEmail1').val().replace(/ /g, '').length > kami) {
        //         necessary($('#exampleInputEmail1').val());
        //     }
        // }, 1500); 
        // clearInterval(checkInterval)