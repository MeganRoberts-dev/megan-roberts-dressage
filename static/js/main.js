document.addEventListener('DOMContentLoaded', () => {
    console.log("About page loaded!");
});

/* Carousel */ 
  var myCarousel = document.getElementById('carouselExampleIndicators')
  var carousel = new bootstrap.Carousel(myCarousel, {
    interval: 5000, // 5 seconds auto-slide
    ride: 'carousel'
  })
