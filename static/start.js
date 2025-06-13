
// script.js

gsap.registerPlugin(ScrollTrigger);

gsap.to("header", { duration: 1, opacity: 1, y: 0 });
gsap.to(".hero", { duration: 1.5, opacity: 1, y: 0, delay: 0.5 });

gsap.to(".arrow-down", {
    duration: 1,
    opacity: 1,
    delay: 1.5,
    repeat: -1,
    yoyo: true,
    y: -10
});

gsap.from(".hero-image img", {
    scrollTrigger: {
        trigger: ".hero-image",
        start: "top 80%",
        end: "bottom 20%",
        scrub: true
    },
    y: 50,
    opacity: 0,
    scale: 0.9 // dodane powiększenie
});

gsap.from(".hero-text", {
    scrollTrigger: {
        trigger: ".hero-text",
        start: "top 80%",
        end: "bottom 20%",
        scrub: true
    },
    y: 30,
    opacity: 0
});
