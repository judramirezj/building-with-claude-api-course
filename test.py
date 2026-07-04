"""
Test file for main.py functions
"""
import math
from main import calculate_pi, calculate_pi_simple


def test_calculate_pi():
    """Test the calculate_pi function with various precision levels"""
    print("Testing calculate_pi function:")
    print("-" * 50)
    
    # Test with 5 digits
    pi_5 = calculate_pi(5)
    print(f"Pi to 5 decimal places: {pi_5:.5f}")
    print(f"Expected (math.pi):     {math.pi:.5f}")
    print(f"Difference:             {abs(pi_5 - math.pi):.10f}")
    
    # Verify it's close to the actual value
    assert abs(pi_5 - math.pi) < 0.00001, "Pi calculation is not accurate to 5 decimal places"
    print("✓ Test passed: Pi is accurate to 5 decimal places\n")
    
    # Test with different precision
    pi_10 = calculate_pi(10)
    print(f"Pi to 10 decimal places: {pi_10:.10f}")
    print(f"Expected (math.pi):      {math.pi:.10f}")
    print(f"Difference:              {abs(pi_10 - math.pi):.15f}")
    print()


def test_calculate_pi_simple():
    """Test the simple pi calculation function"""
    print("Testing calculate_pi_simple function:")
    print("-" * 50)
    
    pi_simple = calculate_pi_simple()
    print(f"Pi (simple):        {pi_simple}")
    print(f"Expected:           3.14159")
    print(f"Actual math.pi:     {math.pi:.5f}")
    
    # Check if it's 3.14159
    assert abs(pi_simple - 3.14159) < 0.000001, "Simple pi calculation failed"
    print("✓ Test passed: calculate_pi_simple returns correct value\n")


def test_pi_digits():
    """Verify the first 5 decimal digits are correct"""
    print("Testing first 5 decimal digits:")
    print("-" * 50)
    
    pi_value = calculate_pi_simple()
    pi_str = f"{pi_value:.5f}"
    expected = "3.14159"
    
    print(f"Calculated: {pi_str}")
    print(f"Expected:   {expected}")
    
    assert pi_str == expected, f"Expected {expected}, got {pi_str}"
    print("✓ Test passed: All 5 decimal digits are correct\n")


def main():
    """Run all tests"""
    print("=" * 50)
    print("Running Pi Calculation Tests")
    print("=" * 50)
    print()
    
    try:
        test_calculate_pi()
        test_calculate_pi_simple()
        test_pi_digits()
        
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
