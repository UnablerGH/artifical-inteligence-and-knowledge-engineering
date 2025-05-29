(define (problem clean1)
  (:domain robot-cleaner)
  (:objects
    pokoj1 pokoj2 pokoj3 - room
    robo - robot
  )
  (:init
    (at robo pokoj1)
    (dirty pokoj1)
    (dirty pokoj2)
    (dirty pokoj3)
  )
  (:goal (and (clean pokoj1) (clean pokoj2) (clean pokoj3)))
)