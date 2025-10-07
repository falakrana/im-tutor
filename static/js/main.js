;(() => {
  const forms = document.querySelectorAll(".needs-validation")
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add("was-validated")
      },
      false,
    )
  })

  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    // Skip animations for users who prefer reduced motion
    return
  }

  const els = document.querySelectorAll(".reveal-up")
  if (!("IntersectionObserver" in window) || els.length === 0) return

  const obs = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible")
          observer.unobserve(entry.target)
        }
      })
    },
    { rootMargin: "0px 0px -10% 0px", threshold: 0.1 },
  )

  els.forEach((el) => obs.observe(el))
})()
