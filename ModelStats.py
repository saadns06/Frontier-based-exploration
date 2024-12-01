import collections
import datetime
import os
import shutil
import tensorflow as tf

class ModelStatsParams:
    def __init__(self,
                 save_model='models/save_model',
                 moving_average_length=50):
        self.save_model = save_model
        self.moving_average_length = moving_average_length
        self.training_images = False
        self.store_trajectory = True


class ModelStats:
    def __init__(self, params: ModelStatsParams, display, force_override=False):
        self.params = params
        self.display = display
        self.trajectory = []
        self.log_value_callbacks = []
        self.log_dir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        # Setup TensorBoard callback with error handling
        try:
            self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=self.log_dir, histogram_freq=10)
            self.tensorboard_callback._train_dir = self.log_dir + "/training"
        except Exception as e:
            print(f"Error initializing TensorBoard callback: {e}")

        # Ensure log directory is clean
        if os.path.isdir(self.log_dir):
            shutil.rmtree(self.log_dir)
        self.training_log_writer = tf.summary.create_file_writer(self.log_dir + '/training')
        self.testing_log_writer = tf.summary.create_file_writer(self.log_dir + '/test')

        self.bar = None
        self.model = None

    def set_model(self, model):
        if model:
            self.tensorboard_callback.set_model(model)
            self.model = model
            print("Model set successfully.")
        else:
            print("No model provided.")

    def add_log_data_callback(self, name: str, callback: callable):
        self.log_value_callbacks.append((name, callback))

    def add_experience(self, experience):
        if self.params.store_trajectory:
            self.trajectory.append(experience)
            if len(self.trajectory) > 1000:  # Limit the size of the trajectory to prevent memory issues
                self.trajectory.pop(0)

    def clear_trajectory(self):
        self.trajectory = []

    def analyze_trajectory(self):
        """
        Analyze the stored trajectory for insights.
        """
        if not self.trajectory:
            print("No trajectory data available.")
            return

        avg_reward = sum(exp['reward'] for exp in self.trajectory) / len(self.trajectory)
        print(f"Average reward per experience: {avg_reward:.2f}")
        print(f"Total experiences logged: {len(self.trajectory)}")

    def log_data(self, step):
        for name, callback in self.log_value_callbacks:
            try:
                value = callback()
                tf.summary.scalar(name, value, step=step)
                print(f"Logged {name}: {value} at step {step}")
            except Exception as e:
                print(f"Error logging {name}: {e}")

    def log_training_data(self, step):
        with self.training_log_writer.as_default():
            self.log_data(step)

    def log_testing_data(self, step):
        with self.testing_log_writer.as_default():
            self.log_data(step)

    def get_log_dir(self):
        return self.log_dir

    def save_model(self):
        if self.model and self.params.save_model != '':
            try:
                self.model.save_weights(self.params.save_model + '_final')
                print(f"Model saved as {self.params.save_model}_final")
            except Exception as e:
                print(f"Error saving model: {e}")

    def training_ended(self):
        self.save_model()
        print("Training has ended. Model saved.")

    def on_episode_begin(self, episode_count):
        self.tensorboard_callback.on_epoch_begin(episode_count)
        self.trajectory = []

    def on_episode_end(self, episode_count):
        self.tensorboard_callback.on_epoch_end(episode_count)
        self.analyze_trajectory()
