(define (domain transport-paczek)
  (:requirements :strips :typing :negative-preconditions :numeric-fluents)
  (:types robot package location)
  (:predicates
    (at ?r - robot ?l - location)
    (at-packet ?p - package ?l - location)
    (connected ?from ?to - location)
  )
  (:action load
    :parameters (?r - robot ?p - package ?l - location)
    :precondition (and (at ?r ?l) (at-packet ?p ?l))
    :effect (and (not (at-packet ?p ?l)) (loaded ?p ?r))
  )
  (:action unload
    :parameters (?r - robot ?p - package ?l - location)
    :precondition (loaded ?p ?r)
    :effect (and (at-packet ?p ?l) (not (loaded ?p ?r)))
  )
  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and (at ?r ?from) (connected ?from ?to))
    :effect (and (not (at ?r ?from)) (at ?r ?to))
  )
)