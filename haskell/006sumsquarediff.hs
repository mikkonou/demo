sumOfSquares = sum [ x^2 | x <- [1..100] ]
squareOfSum = (^2) $ sum [1..100]
diff = squareOfSum - sumOfSquares