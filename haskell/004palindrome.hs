import Data.List

isPalindrome x =
    let numberString = show x
    in numberString == reverse numberString

numbers = reverse $ nub $ sort $ [ x*y | x <- [100..999], y <- [100..999] ]
palindromes = filter (\x -> isPalindrome x) numbers