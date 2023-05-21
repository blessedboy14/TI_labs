package com.example.ti_lab4;

import java.math.BigInteger;
import java.util.*;

public class OperationBox {
    public static boolean isPrime(BigInteger num) {
        if (Objects.equals(num, BigInteger.TWO)) {
            return true;
        }
        Random rand = new Random();
        BigInteger maxValue = num.subtract(BigInteger.TWO);
        for (int i = 0; i < 100; i++) {
            BigInteger a;
            do{
                a = new BigInteger(num.bitLength(), rand);
            } while (a.compareTo(BigInteger.ONE) <= 0 || a.compareTo(maxValue) >= 0);
            if (!Objects.equals(gcd(a, num), BigInteger.ONE))
                return false;
            if(!Objects.equals(pows(a, num.subtract(BigInteger.ONE), num), BigInteger.ONE))
                return false;
        }
        return true;
    }

    public static boolean isLittleNumberPrime(int num) {
        for (int i = 2; i < Math.sqrt(num) + 1; i++) {
            if (num % i == 0) {
                return false;
            }
        }
        return true;
    }

    public static long computeDValue(long eValue, long eulerFunc) {
        long y = 0, true_x = 1, lasty = 1, true_lastx = 0, temp;
        long eulerFuncOld = eulerFunc;
        while (eulerFunc != 0) {
            long quotient = eValue / eulerFunc;
            long modValue = eValue % eulerFunc;
            eValue = eulerFunc;
            eulerFunc = modValue;
            temp = y;
            y = lasty - quotient * y;
            lasty = temp;
            temp = true_x;
            true_x = true_lastx - quotient * true_x;
            true_lastx = temp;
        }
        return (lasty < 0 ? (lasty + eulerFuncOld) : lasty);
    }

    public static long compressInputFile(int H0, int[] inputFile, long rValue) {
        long HOld = H0;
        for (int value: inputFile) {
            long HNew = fastExp(HOld + value, 2, rValue);
            HOld = HNew;
        }
        return HOld;
    }

    private static BigInteger gcd(BigInteger a, BigInteger num) {
        if(Objects.equals(num, BigInteger.ZERO))
            return a;
        return gcd(num, a.mod(num));
    }

    public static boolean isPrimeWith(long numA, long numB) {
        while (numB !=0) {
            long tmp = numA%numB;
            numA = numB;
            numB= tmp;
        }
        return numA == 1;
    }

    private static BigInteger pows(BigInteger base, BigInteger exponent, BigInteger m){
        int trailing_zero_bits_count = exponent.getLowestSetBit();
        if (trailing_zero_bits_count == -1)
            return BigInteger.ONE.mod(m);

        BigInteger z = pows(base, exponent.shiftRight(1), m);
        BigInteger z_sq = z.pow(2).mod(m);
        if (trailing_zero_bits_count != 0)
            return z_sq;
        return z_sq.multiply(base).mod(m);
    }

    private static Set<Integer> findAllPrimeDivisors(int num) {
        Set<Integer> result = new HashSet<>();
        int i = 2;
        while (i*i <= num) {
            if (num % i == 0) {
                result.add(i);
                while (num % i == 0) {
                    num /= i;
                }
            }
            i++;
        }
        if (num > 1) {
            result.add(num);
        }
        return result;
    }

    public static BigInteger bigIntFastExp(BigInteger base, BigInteger pow, BigInteger n) {
        BigInteger x = BigInteger.ONE;
        while (!pow.equals(BigInteger.ZERO)) {
            while (pow.mod(BigInteger.TWO).equals(BigInteger.ZERO)) {
                pow = pow.divide(BigInteger.TWO);
                base = (base.multiply(base)).mod(n);
            }
            pow = pow.subtract(BigInteger.ONE);
            x = (x.multiply(base)).mod(n);
        }
        return x;
    }

    public static void gcdExtended(long a0, long a1) {
        long y = 0, true_x = 1, lasty = 1, true_lastx = 0, temp;
        while (a1 != 0)
        {
            long quotient = a0 / a1;
            long modValue = a0 % a1;

            a0 = a1;
            a1 = modValue;

            temp = y;
            y = lasty - quotient * y;
            lasty = temp;

            temp = true_x;
            true_x = true_lastx - quotient * true_x;
            true_lastx = temp;
            System.out.println("quo = " + quotient + ", a0 =" + a0 + ", a1 = " + a1 + ",y = " + y + ", y1 = " + lasty + ", x = " + true_x + ", x1 = " + true_lastx);
        }
        System.out.println("GCD "+a0+" and its Roots  x : "+ lasty +" y :"+ true_lastx);
    }

    public static long fastExp(long base, int pow, long n) {
        long x = 1;
        long based = base;
        while (pow != 0) {
            while (pow % 2 == 0) {
                pow /= 2;
                based = (based*based) % n;
            }
            pow--;
            x = (x * based) % n;
        }
        return x;
    }

    public static ArrayList<Integer> findPrimitiveRoot(int pNum) {
        int eulerFunc = pNum - 1;
        Set<Integer> primeDivisors = findAllPrimeDivisors(eulerFunc);
        System.out.println(primeDivisors);
        ArrayList<Integer> result = new ArrayList<>();
        boolean isPrimitiveRoot;
        for (int i = 2; i < pNum; i++) {
            isPrimitiveRoot = true;
            for (Integer divisor: primeDivisors) {
                int lPow = eulerFunc/divisor;
                if (fastExp(i, lPow, pNum) == 1) {
                    isPrimitiveRoot = false;
                    break;
                }
            }
            if (isPrimitiveRoot) {
                result.add(i);
            }
        }
        return result;
    }

    public static int[] computeBValue(int[] input, int yValue, int kValue, int pValue) {
        int[] bValue = new int[input.length];
        for (int i = 0; i < input.length; i++) {
            bValue[i] = (int) ((input[i] * fastExp(yValue, kValue, pValue)) % pValue);
        }
        return bValue;
    }

    public static int[] decipherData(int aValue, int[] bValue, int xValue, int pValue) {
        int[] result = new int[bValue.length];
        for (int i = 0; i < bValue.length; i++) {
            result[i] = (int) ((bValue[i] * fastExp(aValue, pValue - 1 - xValue, pValue)) % pValue);
        }
        return result;
    }
}
