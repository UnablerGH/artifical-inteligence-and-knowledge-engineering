(define (problem transport1)
  (:domain transport-paczek)
  (:objects
    loc1 loc2 loc3 - location
    rob1 - robot
    pkg1 pkg2 - package
  )
  (:init
    (at rob1 loc1)
    (at-packet pkg1 loc1)
    (at-packet pkg2 loc2)
    (connected loc1 loc2)
    (connected loc2 loc3)
    (connected loc3 loc1)
  )
  (:goal (and (at-packet pkg1 loc3) (at-packet pkg2 loc1)))
)