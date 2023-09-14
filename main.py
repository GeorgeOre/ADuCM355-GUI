'''
#######################GORECODE#######################
This application is designed to facilitate use of the
ADucM355 evaluation board for electrochemical testing
purposes. It will only allow the execution of square
wave voltammetry and a KDM analysis of the results.

This file outlines the UI structure:
- Begins in a start frame
    - Sets crucial values:
        - Communication port
        = Baud rate
- Main Menu
    - Acts as a hub for the applications various functions
- Settings
    - Allows the user to modify the parameters of the SWV test
- Run Experiment
    - Triggers the board to run the experiment and changes
    settings if necessary
    - Shows a graph of results when finished
    - Saves data as CSV file
- View/Process Data
    -TO DO
#######################GORECODE#######################
'''
import csv
import os
import time
#Packages
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import GoreCom
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#Global Variables
com_port = 'COM3'
baud_rate = 9600
serial_obj = GoreCom.initialize_serial(com_port, baud_rate)

channel = 0
VInitial = 0.0
VFinal = 0.5
VAmplitude = 0.1
VStep = 0.1
Frequency = 300
Equilibrium = 1



class StartFrame(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)

        self.label = tk.Label(self, text="Welcome to the ADuCM355 Testing Inteface")
        self.label.pack(pady=20)


        self.port_label = tk.Label(self, text="Enter Port:")
        self.port_label.pack(pady=20)
        self.port_entry = tk.Entry(self, width=50)
        self.port_entry.pack(pady=20)

        self.baud_label = tk.Label(self, text="Set Baud Rate:")
        self.baud_label.pack(pady=20)
        self.baud_entry = tk.Entry(self, width=50)
        self.baud_entry.pack(pady=20)

        self.start_button = tk.Button(self, text="Save Parameters", command=lambda: self.start(com_port, baud_rate, serial_obj))
        self.start_button.pack()

        self.back_button = tk.Button(self, text="Proceed to Main Menu", command=lambda: switch_frame(MainMenuFrame))
        self.back_button.pack()

    def start(self, p, b, s):
        port = self.port_entry.get()
        baud = self.baud_entry.get()
        p = port
        b = baud
        GoreCom.close_serial(s)
        s = GoreCom.initialize_serial(p, b)

class MainMenuFrame(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)

        self.label = tk.Label(self, text="Main Menu")
        self.label.pack(pady=20)

        self.button1 = tk.Button(self, text="Settings", command=lambda: switch_frame(Frame1))
        self.button1.pack()

        self.button2 = tk.Button(self, text="Run Experiment", command=lambda: switch_frame(Frame2))
        self.button2.pack()

        self.button3 = tk.Button(self, text="Process/View Data", command=lambda: switch_frame(Frame3))
        self.button3.pack()

class Frame1(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)

        self.label = tk.Label(self, text="Settings")
        self.label.grid(row=0, column=3)

        self.note = tk.Label(self, text="*** IMPORTANT ***\n\nSettings must follow\nthe specified format")
        self.note.grid(row=0, column=0)

        self.channel_entry = tk.Entry(self, width=50)
        self.channel_entry.grid(row=1, column=3)
        self.channel_label = tk.Label(self, text="Enter Channel:")
        self.channel_label.grid(row=1, column=2)
        self.channel_label2 = tk.Label(self, text="One character: 0 or 1")
        self.channel_label2.grid(row=1, column=4)

        self.starting_entry = tk.Entry(self, width=50)
        self.starting_entry.grid(row=2, column=3)
        self.starting_label = tk.Label(self, text="Enter Starting Voltage:")
        self.starting_label.grid(row=2, column=2)
        self.starting_label2 = tk.Label(self, text="Five characters: -9999 to +9999")
        self.starting_label2.grid(row=2, column=4)

        self.finishing_entry = tk.Entry(self, width=50)
        self.finishing_entry.grid(row=3, column=3)
        self.finishing_label = tk.Label(self, text="Enter Finishing Voltage")
        self.finishing_label.grid(row=3, column=2)
        self.finishing_label2 = tk.Label(self, text="Five characters: -9999 to +9999")
        self.finishing_label2.grid(row=3, column=4)

        self.amp_entry = tk.Entry(self, width=50)
        self.amp_entry.grid(row=4, column=3)
        self.amp_label = tk.Label(self, text="Enter Amplitude")
        self.amp_label.grid(row=4, column=2)
        self.amp_label2 = tk.Label(self, text="Three characters: 000 to 999")
        self.amp_label2.grid(row=4, column=4)

        self.step_entry = tk.Entry(self, width=50)
        self.step_entry.grid(row=5, column=3)
        self.step_label = tk.Label(self, text="Enter Step")
        self.step_label.grid(row=5, column=2)
        self.step_label2 = tk.Label(self, text="Three characters 000 to 999")
        self.step_label2.grid(row=5, column=4)

        self.freq_entry = tk.Entry(self, width=50)
        self.freq_entry.grid(row=6, column=3)
        self.freq_label = tk.Label(self, text="Enter Frequency")
        self.freq_label.grid(row=6, column=2)
        self.freq_label2 = tk.Label(self, text="Five characters: 00000 to 99999")
        self.freq_label2.grid(row=6, column=4)

        self.eq_entry = tk.Entry(self, width=50)
        self.eq_entry.grid(row=7, column=3)
        self.eq_label = tk.Label(self, text="Enter Equilibrium Time")
        self.eq_label.grid(row=7, column=2)
        self.eq_label2 = tk.Label(self, text="Four characters: 0000 to 9999")
        self.eq_label2.grid(row=7, column=4)

        self.save_button = tk.Button(self, text="Save Settings", command=lambda: self.save(channel, VInitial, VFinal, VAmplitude, VStep, Frequency, Equilibrium))
        self.save_button.grid(row=8, column=3)

        self.back_button = tk.Button(self, text="Back to Main Menu", command=lambda: switch_frame(MainMenuFrame))
        self.back_button.grid(row=9, column=3)

    def save(self, c, st, fh, a, sp, fy, e):
        chan = self.channel_entry.get()
        start = self.starting_entry.get()
        finish = self.finishing_entry.get()
        ampltd = self.amp_entry.get()
        stp = self.step_entry.get()
        freq = self.freq_entry.get()
        eqlbim = self.eq_entry.get()

        GoreCom.send_data(serial_obj, 'c')

        c = chan
        GoreCom.send_data(serial_obj, chan)
        st = start
        GoreCom.send_data(serial_obj, start)
        fh = finish
        GoreCom.send_data(serial_obj, finish)
        a = ampltd
        GoreCom.send_data(serial_obj, ampltd)
        sp = stp
        GoreCom.send_data(serial_obj, stp)
        fy = freq
        GoreCom.send_data(serial_obj, freq)
        e = eqlbim
        GoreCom.send_data(serial_obj, eqlbim)


class Frame2(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)

        self.save_data_button = None
        self.save_graph_button = None
        self.test_button = tk.Button(self, text="Start experiment", command=lambda: (self.add_finished_notification(), self.start_experiment()))
        self.test_button.pack()

        self.serial_data = []  # Placeholder for received serial data
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack()
        self.back_button = tk.Button(self, text="Back to Main Menu", command=lambda: switch_frame(MainMenuFrame))
        self.back_button.pack()

    def add_loading_notification(self):
        # Tell user to wait
        self.loading_label = tk.Label(self, text="Please wait, data loading...")
        self.loading_label.pack()

    def add_finished_notification(self):
        # Tell user to wait
        self.finished_label = tk.Label(self, text="Experiment success!")
        self.finished_label.pack()

    def start_experiment(self):
        GoreCom.send_data(serial_obj, 't')

        # String to store input
        total_input = ''

        # Lists to store data
        voltage_data = []
        current_data = []

        #collect data
        total_input = GoreCom.receive_data2(serial_obj, voltage_data, current_data, total_input)

        # Clear the existing plot
        self.plot.clear()

        # Plot voltage and current data
        self.plot.plot(voltage_data, current_data, marker='o', linestyle='-')
        self.plot.set_title("Voltage vs. Current")
        self.plot.set_xlabel("Voltage (mV)")
        self.plot.set_ylabel("Current (uA)")

        # Update the canvas to show the new plot
        self.canvas.draw()

        # Add options to save image or to save csv
        self.save_graph_button = tk.Button(self, text="Save graph (.png)", command=lambda: self.save_graph())
        self.save_graph_button.pack()
        self.save_data_button = tk.Button(self, text="Save data (.csv)", command=lambda: self.save_data(voltage_data, current_data))
        self.save_data_button.pack()


    def save_graph(self):
        if self.serial_data:
            # Replace this with your code to save the graph
            self.figure.savefig("serial_data_graph.png")
            # Confirm that the image has been saved
            self.image_confirmation = tk.Label(self, text="Image saved as 'serial_data_graph.png'")
            self.image_confirmation.pack()

    def save_data(self, voltage_data, current_data):
        if self.serial_data:
            # Specify the filename for the CSV file
            csv_filename = "data.csv"

            # Combine the voltage and current data into rows
            data_rows = list(zip(voltage_data, current_data))

            # Write the data to the CSV file
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)

                # Write a header row if needed
                writer.writerow(["Voltage (V)", "Current (A)"])

                # Write the data rows
                writer.writerows(data_rows)

            # Confirm that the data has been saved
            self.data_confirmation = tk.Label(self, text="Data saved as 'data.csv'")
            self.data_confirmation.pack()

class Frame3(tk.Frame):
    def __init__(self, master, switch_frame):
        super().__init__(master)

        self.label = tk.Label(self, text="Data Processing Menu")
        self.label.pack(pady=20)

        self.select_directory_button = tk.Button(self, text="Select Directory", command=self.select_directory)
        self.select_directory_button.pack()

        self.search_csv_button = tk.Button(self, text="Perform KDM on CSV Files", command=self.KDM_csv_files)
        self.search_csv_button.pack()

        self.back_button = tk.Button(self, text="Back to Main Menu", command=lambda: switch_frame(MainMenuFrame))
        self.back_button.pack()

        self.selected_directory = ""

    def select_directory(self):
        self.selected_directory = filedialog.askdirectory(title="Select a Directory")

    def KDM_csv_files(self):
        ###################################
        ######### Select the data #########
        ###################################

        if self.selected_directory:
            csv_files = [file for file in os.listdir(self.selected_directory) if file.lower().endswith('.csv')]
            if csv_files:
                print("CSV Files found:")
                for file in csv_files:
                    print(os.path.join(self.selected_directory, file))
                    data = pd.read_csv(file)
                    if file == csv_files[0]:
                        # after reading in our first file we can use the length to declare arrays for the data
                        data_length = len(data)
                        Vstep_data = np.empty([data_length, file])
                        Idif_data = np.empty([data_length, file])
                        print("\nData length is " + str(data_length) + "\n")
                    else:
                        # ignore the statements above on all but the first time through the loop
                        pass
                    Vstep_data[:, file] = data["Vstep"].to_numpy()
                    Idif_data[:, file] = data["Idif"].to_numpy()
            else:
                print("No CSV files found in the selected directory.")
                self.destroy()
        else:
            print("Please select a directory before searching for CSV files.")
            self.destroy()


        ###################################
        ######### Smooth the data #########
        ###################################

        WSZ = 11  # smoothing window size; must be odd number

        for csvfile in range(len(csv_files)):  # each concentration
                Idif_data[:, csvfile] = self.smooth(Idif_data[:, csvfile], WSZ)

        ########################################
        ######### Adjust the baselines, find the peaks #########
        ########################################
        E1 = -0.38  # default values to define the edge of the peak for baseline calc
        E2 = -0.15

        # initialize array to store peak values
        I_peak = np.empty([len(csv_files)])

        for csv_file in range(len(csv_files)):  # each frequency
            Vstep = Vstep_data[:, csv_file]
            Idif = Idif_data[:, csv_file]

            plot_title = f"{csv_files[csv_file]}"

            # show the plot and ask user to pick the lowest "corners" of the peak
            plt.figure()
            plt.plot(Vstep, Idif)
            plt.title(plot_title)
            plt.xlabel("Vstep")
            plt.ylabel("Idif (smoothed)")
            plt.axvline(x=E1, color='y')
            plt.axvline(x=E2, color='y')
            plt.show(block=False)

            try:
                limits = input(
                    'For ' + plot_title + ', input LOWER LIMIT, HIGHER LIMIT (e.g. -0.38, -0.15),\nor hit enter to use the previous values (yellow lines):\n')
                limits = np.sort(eval(limits))
                E1 = limits[0]
                E2 = limits[1]
            except:
                pass
                # use the previous values (set above) if user doesn't enter new values or messes up typing

            plt.close()

            # Use the values at the peak limits to make a polynomial baseline
            # indices of Vstep points within E1 and E2
            peak = np.argwhere((Vstep >= E1) & (Vstep <= E2))
            # split in half (need to evaluate the min separately)
            nn = int(np.ceil(np.size(peak) / 2))
            base1 = np.array(peak[0:nn])
            base2 = np.array(peak[nn:])  # Split E_array in two parts
            y = Idif

            # take an average around each selected limit (otherwise, if data is noisy, that value could vary widely)
            poly_y1 = np.mean(y[int(peak[0] - WSZ): int(peak[0] + WSZ)])
            poly_y2 = np.mean(y[int(peak[-1] - WSZ): int(peak[-1] + WSZ)])
            basefit = np.polyfit([Vstep[int(peak[0])], Vstep[int(peak[-1])]], [
                poly_y1, poly_y2], 1)
            baseline = np.polyval(basefit, Vstep)  # applies to the whole potential V range

            plt.figure()
            plt.plot(Vstep, Idif)
            plt.plot(Vstep, baseline)
            plt.title(plot_title)
            plt.xlabel("Vstep")
            plt.ylabel("Idif (smoothed)")
            plt.axvline(x=E1, color='y')
            plt.axvline(x=E2, color='y')
            plt.show(block=False)

            input('Baseline is plotted. Hit enter to continue\n')
            plt.close()

            # Finally, subtract the baseline from the data
            Idif_data[:, ] = Idif - baseline

            # Find the peak; don't consider anything outside the user-given limits, because those tails can actually be higher than the real peak
            I_peak[csv_file] = max(Idif_data[peak, csv_file])

            plt.title("bruh")
            plt.xlabel("Potential vs Ag|AgCl (V)")
            plt.ylabel("$I_ (A)")
            plt.legend()
            plt.show(block=False)
            input('\nSWV curves are plotted. To save the figure, \nuse the save icon. Hit enter to continue\n')
            plt.close()


        ###########################################
        ######### Calculate and plot KDM  #########
        ###########################################
        KDM_data = np.empty((len(csv_files)))

        off_freq_index =0

        # order of parameters: (lowf_no_targ, lowf_targ, highf_no_targ, highf_targ)
        for c in range(len(csv_files)):
            KDM_data[len(csv_files)] = self.KDM_calc(
                I_peak[0, off_freq_index],  # no target, reference/OFF freq
                I_peak[c, off_freq_index],  # with target, reference/OFF freq
                I_peak[0, :],  # no target, ON frequency
                I_peak[c, :]  # with target, ON frequency
            )

        # print(KDM_data)

        # make the KDM plot
        plt.figure()
        plt.title("KDM vs target concentration:")
        plt.xlabel("Concentration (µM)")
        plt.xscale('symlog')
        # 'symlog' (instead of 'log') makes the interval near zero linear, otherwise there's no data point shown at "0 µM"
        plt.ylabel("KDM")
        plt.plot(1.0, KDM_data[:, :])
        plt.legend()
        plt.show(block=False)
        input('\nKDM data is plotted. To save the figure, use the save icon. Hit enter to continue\n')
        plt.close()


    def smooth(a, WSZ):
        # a: NumPy 1-D array containing the data to be smoothed
        # WSZ: smoothing window size; must be odd number
        # convolves the array with a moving average, cuts off ends that don't have full overlap
        out0 = np.convolve(a, np.ones(WSZ, dtype=int), 'valid') / WSZ
        r = np.arange(1, WSZ - 1, 2)
        start = np.cumsum(a[:WSZ - 1])[::2] / r  # fix the start
        stop = (np.cumsum(a[:-WSZ:-1])[::2] / r)[::-1]  # fix the end
        return np.concatenate((start, out0, stop))  # assemble the ends and middle

    def KDM_calc(lowf_no_targ, lowf_targ, highf_no_targ, highf_targ):
        # peak currents for high/low (on/off) frequencies,
        # with and without target
        hilo_diff = (highf_targ / highf_no_targ) - (lowf_targ / lowf_no_targ)
        hilo_avg = 0.5 * ((highf_targ / highf_no_targ) +
                          (lowf_targ / lowf_no_targ))
        KDM = hilo_diff / hilo_avg
        return KDM


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ADuCM355 Custom Application")
        self.geometry("1100x800")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for FrameClass in (StartFrame, MainMenuFrame, Frame1, Frame2, Frame3):
            frame = FrameClass(self.container, self.switch_frame)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame(StartFrame)

    def switch_frame(self, new_frame):
        frame = self.frames[new_frame]
        for frm in self.frames.values():
            frm.grid_remove()  # Remove all frames from view
        frame.grid()  # Show the selected frame


if __name__ == "__main__":
    app = Application()
    app.mainloop()
