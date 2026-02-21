def number_pattern(n):
    if not isinstance(n, int):
        return "Argument must be an integer value."

    elif n < 1:
        return "Argument must be an integer greater than 0."
    else:
      return " ".join(str(num) for num in range(1, n + 1))

number_pattern(10)
