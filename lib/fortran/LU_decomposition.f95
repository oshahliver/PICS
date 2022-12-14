program lu1
   use linalg

   implicit none

   real(8), dimension(3) :: b1 = (/1, 2, 3/), x1 = (/0.0d0, 0.0d0, 0.0d0/)
   real(8), dimension(4) :: b2 = (/1, 2, 3, 4/), x2 = (/0.0d0, 0.0d0, 0.0d0, 0.0d0/)
   call solve(reshape([real(8)::1, 2, 1, 3, 4, 1, 5, 7, 0], [3, 3]), b1, x1)
   call solve(reshape([real(8)::11, 1, 3, 2, 9, 5, 17, 5, 24, 2, 18, 7, 2, 6, 1, 1], [4, 4]), b2, x2)

contains

   subroutine solve(a, b, x)
      real(8), intent(in)   :: a(:, :)
      real(8), intent(inout) :: b(:), x(:)
      integer               :: i, j, n
      real(8), allocatable  :: aa(:, :), l(:, :), u(:, :)
      real(8), allocatable  :: p(:, :)
      integer, allocatable  :: ipiv(:)

      n = size(a, 1)

      allocate (aa(n, n), l(n, n), u(n, n), p(n, n), ipiv(n))

      forall (j=1:n, i=1:n)
         aa(i, j) = a(i, j)
         u(i, j) = 0d0
         p(i, j) = merge(1, 0, i .eq. j)
         l(i, j) = merge(1d0, 0d0, i .eq. j)
      end forall

      call lu(aa, ipiv)

      do i = 1, n
         l(i, :i - 1) = aa(ipiv(i), :i - 1)
         u(i, i:) = aa(ipiv(i), i:)
      end do

      p(ipiv, :) = p

      call backward_substitution(l, b, 'lower')
      call backward_substitution(u, b, 'upper')
      call matrix_multiplication(n=n, m=n, l=1, a1=p, a2=b, a=x)

      !call mat_print('a',a)
      !call mat_print('p',p)
      !call mat_print('l',l)
      !call mat_print('u',u)

      !print *, "residual"
      !print *, "|| P.A - L.U || =  ", maxval(abs(matmul(p,a)-matmul(l,u)))
   end subroutine

   subroutine lu(a, p)
!   in situ decomposition, corresponds to LAPACK's dgebtrf
      real(8), intent(inout) :: a(:, :)
      integer, intent(out) :: p(:)
      integer                :: n, i, j, k, kmax
      n = size(a, 1)
      p = [(i, i=1, n)]
      do k = 1, n - 1
         kmax = maxloc(abs(a(p(k:), k)), 1) + k - 1
         if (kmax /= k) p([k, kmax]) = p([kmax, k])
         a(p(k + 1:), k) = a(p(k + 1:), k)/a(p(k), k)
         forall (j=k + 1:n) a(p(k + 1:), j) = a(p(k + 1:), j) - a(p(k + 1:), k)*a(p(k), j)
      end do
   end subroutine

   subroutine backward_substitution(matrix, sol, type)
      real(8), intent(in) :: matrix(:, :)
      real(8), intent(inout) :: sol(:)
      character(len=5), intent(in) :: type
      integer :: n, i, j
      n = size(matrix, 1)

      if (type == 'lower') then
      do i = 1, n

         !sol(ind) = sol(ind)
         do j = 1, i - 1
            sol(i) = sol(i) - matrix(i, j)*sol(j)
         end do
         sol(i) = sol(i)/matrix(i, i)
      end do

      elseif (type == 'upper') then
      do i = 1, n
         !sol(ind) = sol(ind)
         do j = 1, i - 1
            sol(n - i + 1) = sol(n - i + 1) - matrix(n - i + 1, n - j + 1)*sol(n - j + 1)
         end do
         sol(n - i + 1) = sol(n - i + 1)/matrix(n - i + 1, n - i + 1)
      end do
      end if

   end subroutine backward_substitution

   subroutine mat_print(amsg, a)
      character(*), intent(in) :: amsg
      class(*), intent(in) :: a(:, :)
      integer                  :: i
      print *, ' '
      print *, amsg
      do i = 1, size(a, 1)
         select type (a)
         type is (real(8)); print'(100f8.2)', a(i, :)
         type is (integer); print'(100i8  )', a(i, :)
         end select
      end do
      print *, ' '
   end subroutine

end program
