def find_affine_points(a, b, p):
    points = []
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        if pow(y_squared, (p - 1) // 2, p) == 1 or y_squared == 0:
            for y in range(p):
                if (y * y) % p == y_squared:
                    points.append((x, y))
    return points

a, b, p = 1, 1, 23

affine_points = find_affine_points(a, b, p)
print("Affine points on the curve:")
for point in affine_points:
    print(point)

print(f"\nTotal affine points: {len(affine_points)}")