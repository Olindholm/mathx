
import math

# Cache for fast lookup
primes = []

def prime_number(n, clear_cache=False):
    """
    Return the nth prime number.

    Parameters
    ----------
    n : int
        The nth prime number, e.g. the first prime is 2, and second is 3.
        For more info see [List of prime numbers on wikipedia](https://en.wikipedia.org/wiki/List_of_prime_numbers).

    clear_cache : bool, default False
        This function uses a shared cache to calculate the prime numbers.
        This allows much faster latter executions. Set this to `True` if
        you want to clear the cache after the function is finished.

        This will clear all shared cache, and result in later executions
        being a lot slower.

    Returns
    -------
    prime : int
        The nth prime number.

    Raises
    ------
    TypeError
        If n is not an integer.
    ValueError
        If n is not strictly positive.
    """

    # Ensure n is a integer
    if (not isinstance(n, int)):
        raise TypeError("n must be an integer!")

    # Ensure n is positive
    if (n <= 0):
        raise ValueError("n must be a strictly positive!")

    i = primes[-1] if len(primes) > 0 else 1
    while len(primes) < n:
        i += 1
        sqrtOfI = math.isqrt(i)

        # Assume it is a prime
        isPrime = True

        for prime in primes:
            if (prime > sqrtOfI): break
            if (i % prime == 0):
                # If the remainder is 0, it is not a prime.
                isPrime = False
                break

        if (isPrime):
            primes.append(i)

    # Get prime number n
    prime = primes[n-1]

    # Clear cache
    if (clear_cache):
        primes.clear()

    # Return result
    return prime
