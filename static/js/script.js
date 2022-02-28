  //   var elemets = document.querySelector('.card');
  let element = document.getElementById('show')
  element.addEventListener("click", myFunction);
  element.addEventListener("mouseout", myFun);

  let el = document.getElementById('nav')
  el.addEventListener("click", myNav);
  // el.addEventListener("mouseout", myNavO);
  function myNav() {
      anime({
          targets: '#nav',
          padding: 10,
          translateY: [
              { value: 20, duration: 1000, easing: 'easeOutSine' }
          ],
          delay: anime.stagger(100),
      })
  }
  // function myNavO() {
  //     anime({
  //         targets: '#nav',
  //         translateY: [
  //             { value: 0, duration: 1000, easing: 'easeOutSine' }
  //         ],
  //         delay: anime.stagger(100),
  //     })
  // }
  function myFunction() {
      anime({
          targets: '.show',
          translateY: [
              { value: -250, duration: 1000, easing: 'easeOutSine' }
          ],
          delay: anime.stagger(100),
      })
  }
  function myFun() {
      anime({
          targets: '.show',
          translateY: [
              { value: 0, duration: 1000, easing: 'easeOutSine' }
          ],
          delay: anime.stagger(100),
      })
  }
  anime({
      targets: '.card ,.card1',
      translateY: [
          { value: 200, duration: 1000, easing: 'easeOutSine' },
          { value: -100, duration: 1000, easing: 'easeOutSine' },
          { value: 0, duration: 1000, easing: 'easeOutSine' }
      ],

      delay: anime.stagger(200, { grid: [16, 10], from: 7 }),
      loop: false
  })