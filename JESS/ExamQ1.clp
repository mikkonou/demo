;Mikko Nousiainen

(clear)
(reset)

(defglobal ?*excellent* = 4)
(defglobal ?*good* = 3)
(defglobal ?*acceptable* = 2)
(defglobal ?*poor* = 1)

(deftemplate car
    (slot name (type string))
	(slot condition (type integer))
    (slot driven (type integer))
    (slot age (type integer))
)

(defrule display_inside_less_than_2_years
	(declare (salience 3))
    ?car <- (car (name ?name) (condition ?condition) (age ?age))
    (test (<= ?age 2))
    (test (or (eq ?condition ?*good*) (eq ?condition ?*excellent*)))
    =>
    (printout t ?name " should be displayed inside." crlf)
    (retract ?car)
)

(defrule display_inside_less_than_3_years
	(declare (salience 2))
    ?car <- (car (name ?name) (condition ?condition) (driven ?driven) (age ?age))
    (test (<= ?age 3))
    (test (< ?driven 120000))
    (test (or (eq ?condition ?*acceptable*) (eq ?condition ?*good*) (eq ?condition ?*excellent*)))
    =>
    (printout t ?name " should be displayed inside." crlf)
    (retract ?car)
)

(defrule display_inside_less_than_5_years
	?car <- (car (name ?name) (condition ?condition) (driven ?driven) (age ?age))
    (test (<= ?age 5))
    (test (< ?driven 120000))
    (test (or (eq ?condition ?*good*) (eq ?condition ?*excellent*)))
    =>
    (printout t ?name " should be displayed inside." crlf)
    (retract ?car)
)

(defrule display_outside
	?car <- (car (name ?name) (condition ?condition) (driven ?driven))
    (test (> ?driven 200000))
    (test (or (eq ?condition ?*acceptable*) (eq ?condition ?*good*) (eq ?condition ?*excellent*)))
    =>
    (printout t ?name " should be displayed outside." crlf)
    (retract ?car)
)

(defrule poor_condition_sell_to_low_end_dealer
	?car <- (car (name ?name) (condition ?condition))
    (test (or (eq ?condition ?*poor*)))
    =>
    (printout t ?name " should be sold to low end dealer." crlf)
    (retract ?car)
)
    
(defrule no_applicable_conditions
	(declare (salience -10))
    ?car <- (car (name ?name))
    =>
    (printout t ?name " should be sold to low end dealer." crlf)
    (retract ?car)
)

(assert (car (name "upx 668" ) (condition ?*good*) (driven 260000) (age 7)))
(assert (car (name "fyi 123" ) (condition ?*good*) (driven 132000) (age 1)))
(assert (car (name "foo 856" ) (condition ?*good*) (driven 75000) (age 3)))
(assert (car (name "gif 856" ) (condition ?*poor*) (driven 75000) (age 3)))
(assert (car (name "gui 352" ) (condition ?*acceptable*) ( driven 83200) ( age 3)))
(assert (car (name "bar 669" ) (condition ?*good*) (driven 75000) (age 8)))
(assert (car (name "swf 483" ) (condition ?*good*) (driven 120000) (age 4)))
(assert (car (name "lzw 632" ) (condition ?*acceptable*) ( driven 110000) ( age 4)))
(assert (car (name "exe 994" ) (condition ?*good*) (driven 270000) (age 3)))
(assert (car (name "cab 129" ) (condition ?*good*) (driven 238000) (age 2)))
(assert (car (name "pum 123" ) (condition ?*poor*) (driven 120000) (age 3)))
(assert (car (name "huf 673" ) (condition ?*poor*) (driven 210000) (age 7)))

(run 20)
