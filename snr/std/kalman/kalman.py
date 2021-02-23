import numpy as np
from snr.types.base import *

SymbolicParamGetter = Callable[[float], np.ndarray]


def matrix(*args: Any) -> np.ndarray:
    return np.array([*args])


@dataclass
class Correction:
    k: np.ndarray
    x: np.ndarray
    p: np.ndarray


@dataclass
class Prediction:
    x: np.ndarray
    p: np.ndarray


class KalmanFilter:
    def __init__(self,
                 calc_phi: SymbolicParamGetter,
                 calc_q: SymbolicParamGetter,
                 h: np.ndarray,
                 r: np.ndarray):
        self.calc_phi = calc_phi
        self.calc_q = calc_q
        self.h = h
        self.r = r
        self.I_state = np.identity(len(h[0]))

    def get_phi(self, delta_t: float) -> np.ndarray:
        return self.calc_phi(delta_t)

    def get_q(self, delta_t: float) -> np.ndarray:
        return self.calc_q(delta_t)

    # % Identify number of measurements
    # iterations = length(delta_time);

    # % Identify number and location of position state variables
    pos_x_state = np.array([1, 0, 0, 0, 0, 0])
    pos_y_state = np.array([0, 0, 1, 0, 0, 0])
    # pos_z_state = np.array([0, 0, 0, 0, 1, 0])

    # % Calculate velocities per dimension
    # vel_x = pos_x(2:iterations)' - pos_x(1:iterations-1)';
    # vel_y = pos_y(2:iterations)' - pos_y(1:iterations-1)';
    # vel_z = pos_z(2:iterations)' - pos_z(1:iterations-1)';

    # % Store position and velocity measurements
    # z = [pos_x(:)';
    #      0 vel_x(:)';
    #      pos_y(:)';
    #      0 vel_y(:)';
    #      pos_z(:)';
    #      0 vel_z(:)'];

    # % Set up symbolic PV systems
    # syms dt q;
    # Phi_pv = [1 dt;
    #           0  1];
    # Q_pv = [q*(dt^3)/3 q*(dt^2);
    #         q*(dt^2)/2     q * dt];
    # zero = zeros(2, 2);

    # % Construct Phi and Q from symbolic systems for each dimension
    # phi = [Phi_pv zero   zero;
    #        zero   Phi_pv zero;
    #        zero   zero   Phi_pv];
    # Q = [Q_pv  zero  zero;
    #      zero  Q_pv  zero;
    #      zero  zero  Q_pv];

    # % Set model parameters
    # q = 100;
    # params.Phi = matlabFunction(phi); % Treat symbolic systems as a function
    # params.Q = matlabFunction(subs(Q, q));
    # params.H = [pos_x_state; pos_y_state; pos_z_state];
    # params.R = diag([var(pos_x) var(pos_y) var(pos_z)]);

    # % Run filter
    # [xs, P, e] = run_filter(params, z, delta_time);

    def correct(self,
                delta_t: float,
                z: np.ndarray,
                prediction: Prediction
                ) -> Correction:
        #  % Kk = p_min * H' / (H * p_min * H' + R);
        Kk = prediction.p @ np.transpose(self.h) / \
            (self.h @
             prediction.p @
             np.transpose(self.h) + self.r)
        #  % x = x_min + Kk * (z - H * x_min);
        x = prediction.x + Kk @ (z - self.h @ prediction.x)
        #  % p = (params.I_state - Kk * H) * p_min;
        p = (self.I_state - Kk @ self.h) * prediction.p
        return Correction(Kk, x, p)

    def predict(self, delta_t: float, correction: Correction) -> Prediction:
        phi = self.get_phi(delta_t)
        #  % x_min_1 = Phi * x;
        x_min_1 = phi @ correction.x
        #  % p_min_1 = Phi * p * Phi' + Q;
        p_min_1 = phi @ correction.p @ np.transpose(phi) + self.get_q(delta_t)
        return Prediction(x_min_1, p_min_1)

    def iterate(self,
                prediction: Prediction,
                dt: float,
                measurement: np.ndarray
                ) -> Tuple[Correction, Prediction]:
        # % Iterate over one cycle of the Kalman filter
        # function [Kk, x, p, x_min_1, p_min_1, e] ...
        #     = iterate(params, Z, delta_t, x_min, p_min)
        #     % Unpack parameters
        #     Phi = params.Phi(delta_t);
        #     Q = params.Q(delta_t);
        #     H = params.H;
        #     R = params.R;
        #     z = [Z(1); Z(3); Z(5)];
        #     % Calculate error
        #     expected = Z;
        #     e = (expected - x).^2;
        correction = self.correct(dt, measurement, prediction)
        prediction = self.predict(dt, correction)
        return correction, prediction

        # % Run the Kalman filter for all available data
        # function [xs, P, e] = run_filter(params, z, delta_time)
    def run_filter(self):
        #     % Unpack parameters
        #     i = length(z(1, :));
        #     state_len = length(params.H(1, :));
        #     measure_len = length(params.H(:, 1));
        #     params.I_state = eye(state_len, state_len);
        #     % Preallocate results
        #     P_min = zeros(state_len, state_len, i);     % P apriori
        #     P     = zeros(state_len, state_len, i);     % P
        #     X_min = zeros(state_len, i);                % X apriori estimate
        #     xs    = zeros(state_len, i);                % X estimate
        #     K     = zeros(state_len, measure_len, i);   % Kalman gain
        #     e     = zeros(state_len, i);                % Error
        #     % Set initial estimates
        #     X_min(:, 1) = z(:, 1);
        #     P_min(:, :, 1) = diag(var(z, 0, 2));
        #     % Iterate over measurements
        #     for k = 1:i
        #         [K(:, :, k), ...
        #          xs(:, k), ...
        #          P(:, :, k), ...
        #          X_min(:, k+1), ...
        #          P_min(:, :, k+1), ...
        #          e(:, k) ...
        #          ] = iterate(params, z(:, k),...
        #                      delta_time(k),...
        #                      X_min(:, k),...
        #                      P_min(:, :, k));
        pass

    def plot(self):
        # % Display results
        # figure(1);
        # grid on
        # hold on
        # for i = 1:q_i
        #     plot(time_s, e_q(1, :, i));
        # end
        # hold off
        # legend(q_legend);
        # title("X position estimate mean squared error");
        # xlabel("Time (seconds)");
        # ylabel("error squared");

        # figure(2);
        # grid on
        # hold on
        # for i = 1:q_i
        #     plot(time_s, e_q(3, :, i));
        # end
        # hold off
        # legend(q_legend);
        # title("Y position estimate mean squared error");
        # xlabel("Time (seconds)");
        # ylabel("error squared");

        # figure(3);
        # grid on
        # hold on
        # for i = 1:q_i
        #     plot(time_s, e_q(5, :, i));
        # end
        # hold off
        # legend(q_legend);
        # title("Altitude estimate mean squared error");
        # xlabel("Time (seconds)");
        # ylabel("error squared");

        # figure(4);
        # grid on
        # hold on
        # for i = 1:q_i
        #     plot(time_s, squeeze(P_q(1, 1, :, i)));
        # end
        # hold off
        # legend(q_legend);
        # title("X position P");
        # xlabel("Time (seconds)");
        # ylabel("Estimate error variance");

        # figure(5);
        # grid on
        # hold on
        # for i = 1:q_i
        #     plot(time_s, squeeze(P_q(3, 3, :, i)));
        # end
        # hold off
        # legend(q_legend);
        # title("Y position P");
        # xlabel("Time (seconds)");
        # ylabel("Estimate error variance");

        # figure(6);
        # grid on
        # hold on
        # for i = 1:q_i
        #     plot(time_s, squeeze(P_q(5, 5, :, i)));
        # end
        # hold off
        # legend(q_legend);
        # title("Altitude P");
        # xlabel("Time (seconds)");
        # ylabel("Estimate error variance");
        pass


def pv_2d(sigma: List[float]) -> KalmanFilter:
    def calc_phi(dt: float) -> np.ndarray:
        return (matrix([1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]) +
                + (matrix([0, 1, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 1],
                          [0, 0, 0, 0])
                   * dt))

    def calc_q(dt: float) -> np.ndarray:
        return matrix([(dt ** 3) / 3, (dt ** 2) / 2, 0, 0],
                      [(dt ** 2) / 2, dt, 0, 0],
                      [0, 0, (dt ** 3) / 3, (dt ** 2) / 2],
                      [0, 0, (dt ** 2) / 2, dt])

    h = matrix([1, 0, 0, 0],
               [0, 0, 1, 0])

    r = matrix([sigma[0]],
               [sigma[1]],
               [sigma[2]],
               [sigma[3]])

    return KalmanFilter(calc_phi, calc_q, h, r)
