# Importing Modules:
from tkinter import filedialog, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter as tk
import math
import cmath
import numpy as np

root = tk.Tk()
mainColor = '#0091D5'
foreColor = '#000000'
geometry_width = 1000
geometry_height = 700
samples1 = []
samples2 = []


# Defined Functions:
    
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def displaySignals(current, discrete_fig, analog_fig):
    graphFrame = tk.Frame(current, bg=mainColor, height=1)

    canvas = FigureCanvasTkAgg(discrete_fig, master=graphFrame)
    canvas.get_tk_widget().grid(row=0, column=0, padx=30,sticky="nsew")

    canvas2 = FigureCanvasTkAgg(analog_fig, master=graphFrame)
    canvas2.get_tk_widget().grid(row=0, column=1, padx=30,sticky="nsew")

    graphFrame.columnconfigure(0, weight=1)
    graphFrame.columnconfigure(1, weight=1)

    # Use the pack geometry manager to fill the available space
    graphFrame.pack(fill=tk.X,expand=False)



def back(current):
    global samples1, samples2
    samples1 = samples2 = []
    current.destroy()


def createBackBtn(current):
    backBtn = Button(current, bg=foreColor, text='Back', font=('Arial', 10), fg='white',
                     width=10, height=1, command=lambda: back(current))
    backBtn.place(x=10, y=10)


# Task::1
def readSamples():
    # 1st part
    root.deiconify()
    first_window = tk.Toplevel()
    center_window(first_window, geometry_width, geometry_height)
    first_window.resizable(False, False)
    first_window.configure(bg=mainColor)
    first_window.title("Reading signals")

    createBackBtn(first_window)

    browseBtn = Button(first_window, bg=foreColor, fg='white',
                       text="Browse", width=20, font=('Arial', 15), command=lambda: browseFiles(first_window))
    browseBtn.pack(pady=10)

    first_window.mainloop()


def browseFiles(current):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if filename:
        textbox = tk.Text(current, height=1, width=150, )
        textbox.insert(tk.END, filename)
        textbox.pack(padx=25, pady=25)
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Extracting the values from the file
        signal_type = int(lines[0].strip())
        is_periodic = int(lines[1].strip())
        n1 = int(lines[2].strip())

        samples = []
        for line in lines[3:]:
            values = line.strip().split()
            if signal_type == 0:  # Time domain
                index = int(values[0])
                amplitude = float(values[1])
                samples.append((index, amplitude))
            elif signal_type == 1:  # Frequency domain
                frequency = float(values[0])
                amplitude = float(values[1])
                phase_shift = float(values[2])
                samples.append((frequency, amplitude, phase_shift))

        if signal_type == 0:  # Time domain
            indices = [sample[0] for sample in samples]
            amplitudes = [sample[1] for sample in samples]
            fig, ax = plt.subplots()
            fig2, ax2 = plt.subplots()
            ax.set_title('Digital representation')
            ax2.set_title('Analog representation')

            # discrete
            ax.stem(indices, amplitudes)
            ax.set_xlabel('Index')
            ax.set_ylabel('Amplitude')
            # continous
            ax2.plot(indices, amplitudes)
            ax2.set_xlabel('Index')
            ax2.set_ylabel('Amplitude')

        elif signal_type == 1:  # Frequency domain
            frequencies = [sample[0] for sample in samples]
            amplitudes = [sample[1] for sample in samples]
            phase_shifts = [sample[2] for sample in samples]

            # discrete
            ax.stem(frequencies, amplitudes)
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Amplitude')
            # continous
            ax2.plot(frequencies, amplitudes)
            ax2.set_xlabel('Frequency')
            ax2.set_ylabel('Amplitude')

        displaySignals(current, fig, fig2)


def generateSinCosSignals():
    # 2nd part
    root.deiconify()
    second_window = tk.Toplevel()
    center_window(second_window, geometry_width, geometry_height)
    second_window.resizable(False, False)
    second_window.configure(bg=mainColor)
    second_window.title("sin/cos signals")

    createBackBtn(second_window)

    btnWithGetterFrame = tk.Frame(second_window, bg=mainColor)
    getterFrame = tk.Frame(btnWithGetterFrame, bg=mainColor)

    label1 = tk.Label(getterFrame, text="sin/cos", bg=mainColor, fg=foreColor)
    label1.grid(row=0, column=0)

    t_type_tbox = tk.Entry(getterFrame, font=(
        'Arial', 10), bg='white', fg='black', )
    t_type_tbox.grid(row=0, column=1)

    label2 = tk.Label(getterFrame, text="Amplitude",
                      bg=mainColor, fg=foreColor)
    label2.grid(row=1, column=0)
    A_tbox = tk.Entry(getterFrame, font=(
        'Arial', 10), bg='white', fg='black', )
    A_tbox.grid(row=1, column=1)

    label3 = tk.Label(getterFrame, text="Analog Frequency ",
                      bg=mainColor, fg=foreColor)
    label3.grid(row=2, column=0)
    AnalogFrequency_tbox = tk.Entry(
        getterFrame, font=('Arial', 10), bg='white', fg='black', )
    AnalogFrequency_tbox.grid(row=2, column=1)

    label4 = tk.Label(getterFrame, text="Sampling Frequency",
                      bg=mainColor, fg=foreColor)
    label4.grid(row=3, column=0)

    SamplingFrequency_tbox = tk.Entry(
        getterFrame, font=('Arial', 10), bg='white', fg='black', )
    SamplingFrequency_tbox.grid(row=3, column=1)

    label5 = tk.Label(getterFrame, text="Phase Shift",
                      bg=mainColor, fg=foreColor)
    label5.grid(row=4, column=0)
    PhaseShift_tbox = tk.Entry(getterFrame, font=(
        'Arial', 10), bg='white', fg='black', )
    PhaseShift_tbox.grid(row=4, column=1)

    getterFrame.grid(row=0, column=0)

    generateBtn = Button(btnWithGetterFrame, bg=foreColor, fg='white', text="Generate",
                         width=15, height=5, font=('Arial', 15),
                         command=lambda: waveGenerator(
                             t_type_tbox, A_tbox, AnalogFrequency_tbox, SamplingFrequency_tbox, PhaseShift_tbox,
                             second_window))
    generateBtn.grid(row=0, column=1, padx=25)

    btnWithGetterFrame.pack(padx=25, pady=25)

    second_window.mainloop()


def waveGenerator(t_type_tbox, A_tbox, AnalogFrequency_tbox, SamplingFrequency_tbox, PhaseShift_tbox, second_window):
    if (t_type_tbox.get() == '' or A_tbox.get() == '' or AnalogFrequency_tbox.get() == ''
            or SamplingFrequency_tbox.get() == '' or PhaseShift_tbox.get() == ''):
        return

    t_type = str(t_type_tbox.get())
    A = int(A_tbox.get())
    AnalogFrequency = int(AnalogFrequency_tbox.get())
    SamplingFrequency = int(SamplingFrequency_tbox.get())
    PhaseShift = float(PhaseShift_tbox.get())

    indecies = []
    samples = []
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')

    if t_type == "sin":
        for i in range(int(SamplingFrequency)):
            indecies.append(i)
            samples.append(A * math.sin(
                (2 * math.pi * (AnalogFrequency / SamplingFrequency) * i) + PhaseShift))

        # discrete
        ax.stem(indecies, samples)
        ax.set_xlabel('Index')
        ax.set_ylabel('Amplitude')
        # continous
        ax2.plot(indecies, samples)
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Amplitude')

        print('sin')
        displaySignals(second_window, fig, fig2)

        SignalSamplesAreEqual('Task 1/SinOutput.txt', indecies, samples)
    elif t_type == "cos":
        for i in range(int(SamplingFrequency)):
            indecies.append(i)
            samples.append(A * math.cos(
                (2 * math.pi * (AnalogFrequency / SamplingFrequency) * i) + PhaseShift))

        # discrete
        ax.stem(indecies, samples)
        ax.set_xlabel('Index')
        ax.set_ylabel('Amplitude')
        # continous
        ax2.plot(indecies, samples)
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Amplitude')
        print('cos')
        SignalSamplesAreEqual('Task 1/CosOutput.txt', indecies, samples)
        displaySignals(second_window, fig, fig2)
    else:
        print("index error:type either sin/cos")


def SignalSamplesAreEqual(file_name, indices, samples):
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break

    if len(expected_samples) != len(samples):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print(
                "Test case failed, your signal have different values from the expected one")
            return
    print("Test case passed successfully")


# Task::2
def Adder():
    root.deiconify()
    third_window = tk.Toplevel()
    center_window(third_window, geometry_width, geometry_height)

    third_window.resizable(False, False)
    third_window.configure(bg=mainColor)
    third_window.title("Adder")

    buildGettingTwoSignals(third_window, 'add')
    createBackBtn(third_window)
    third_window.mainloop()


def buildGettingTwoSignals(window, task):
    splitted_frame = tk.Frame(window, bg=mainColor)
    left_frame = tk.Frame(splitted_frame, )
    left_frame.grid(row=0, column=0, padx=30)
    right_frame = tk.Frame(splitted_frame, )
    right_frame.grid(row=0, column=1, padx=30)
    splitted_frame.pack(padx=10, pady=10)
    # Left side
    leftLabel = tk.Label(left_frame, text='Signal#1', font=('Arial', 15))
    leftLabel.pack(padx=10)
    browseBtnleft = Button(left_frame, bg=foreColor, fg='white',
                           text="Browse", width=20, font=('Arial', 15),
                           command=lambda: getSignal_destroyBtn(left_frame, browseBtnleft, window, task))
    browseBtnleft.pack(pady=10)
    # Right Side
    RightLabel = tk.Label(right_frame, text='Signal#2', font=('Arial', 15))
    RightLabel.pack(padx=10)
    browseBtnright = Button(right_frame, bg=foreColor, fg='white',
                            text="Browse", width=20, font=('Arial', 15),
                            command=lambda: getSignal_destroyBtn(right_frame, browseBtnright, window, task))
    browseBtnright.pack(pady=10)


def getSignal_destroyBtn(current, btn, window, task):
    global samples1, samples2

    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if filename:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Extracting the values from the file
        signal_type = int(lines[0].strip())
        is_periodic = int(lines[1].strip())
        n1 = int(lines[2].strip())

        samples = []
        fig, ax = plt.subplots()
        fig2, ax2 = plt.subplots()
        ax.set_title('Digital representation')
        ax2.set_title('Analog representation')

        for line in lines[3:]:
            values = line.strip().split()
            if signal_type == 0:  # Time domain
                index = int(values[0])
                amplitude = float(values[1])
                samples.append((index, amplitude))
            elif signal_type == 1:  # Frequency domain
                frequency = float(values[0])
                amplitude = float(values[1])
                phase_shift = float(values[2])
                samples.append((frequency, amplitude, phase_shift))
        
        samples.append((is_periodic))

        if signal_type == 0:  # Time domain
            indices = [sample[0] for sample in samples[:-1]]
            amplitudes = [sample[1] for sample in samples[:-1]]

            # discrete
            ax.stem(indices, amplitudes)
            ax.set_xlabel('Index')
            ax.set_ylabel('Amplitude')
            # continous
            ax2.plot(indices, amplitudes)
            ax2.set_xlabel('Index')
            ax2.set_ylabel('Amplitude')

        elif signal_type == 1:  # Frequency domain
            frequencies = [sample[0] for sample in samples[:-1]]
            amplitudes = [sample[1] for sample in samples[:-1]]
            phase_shifts = [sample[2] for sample in samples[:-1]]

            # discrete
            ax.stem(frequencies, amplitudes)
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Amplitude')
            # continous
            ax2.plot(frequencies, amplitudes)
            ax2.set_xlabel('Frequency')
            ax2.set_ylabel('Amplitude')

        btn.destroy()
        if (task == 'add' or task == 'sub' or task=='convolve' or task=='correlate' or task=='fast_convolve' or task=='fast_correlate'):
            figure = FigureCanvasTkAgg(fig2, master=current)
            figure.get_tk_widget().pack()
            if (samples1 == []):
                samples1 = samples
            elif (samples2 == []):
                samples2 = samples
            if (samples1 != [] and samples2 != []):
                if (task == 'add'):
                    addBtn = Button(window, text='Add', bg=foreColor, fg='white',
                                    width=150, font=('Arial', 15), command=lambda: add(window, addBtn))
                    addBtn.pack(padx=30)
                elif (task == 'sub'):
                    subBtn = Button(window, text='Subtract', bg=foreColor, fg='white',
                                    width=150, font=('Arial', 15), command=lambda: sub(window, subBtn))
                    subBtn.pack(padx=30)
                elif (task == 'convolve'):
                    conBtn = Button(window, text='Convolve', bg=foreColor, fg='white',
                                    width=150, font=('Arial', 15), command=lambda: convolve(window, conBtn))
                    conBtn.pack(padx=30) 
                elif (task == 'correlate'):
                    corrBtn = Button(window, text='Compute Normalized Correlation', bg=foreColor, fg='white',
                                    width=150, font=('Arial', 15), command=lambda: correlation(window, corrBtn))
                    corrBtn.pack(padx=30) 
                elif (task == 'fast_convolve'):
                    fastconBtn = Button(window, text='Fast Convolve', bg=foreColor, fg='white',
                                    width=150, font=('Arial', 15), command=lambda: fast_convolve(window, fastconBtn))
                    fastconBtn.pack(padx=30) 
                elif (task == 'fast_correlate'):
                    fastcorrBtn = Button(window, text='Compute Fast Correlation', bg=foreColor, fg='white',
                                    width=150, font=('Arial', 15), command=lambda: fast_correlation(window, fastcorrBtn))
                    fastcorrBtn.pack(padx=30) 
                    
        elif (task == 'multiply'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            multiplyBtn = Button(window, text='Multiply', bg=foreColor, fg='white',
                                 width=150, font=('Arial', 15), command=lambda: multiply(window, multiplyBtn))
            multiplyBtn.pack(padx=30, pady=10)
        elif (task == 'square'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            squareBtn = Button(window, text='Square', bg=foreColor, fg='white',
                               width=150, font=('Arial', 15), command=lambda: square(window, squareBtn))
            squareBtn.pack(padx=30, pady=10)
        elif (task == 'shift'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            shiftBtn = Button(window, text='Shift', bg=foreColor, fg='white',
                              width=150, font=('Arial', 15), command=lambda: shift(window, shiftBtn))
            shiftBtn.pack(padx=30, pady=10)
        elif (task == 'normalize'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            normalizeBtn = Button(window, text='Normalize', bg=foreColor, fg='white',
                                  width=150, font=('Arial', 15), command=lambda: normalize(window, normalizeBtn))
            normalizeBtn.pack(padx=30, pady=10)
        elif (task == 'accum'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            accumBtn = Button(window, text='Accumlate', bg=foreColor, fg='white',
                              width=150, font=('Arial', 15), command=lambda: accum(window, accumBtn))
            accumBtn.pack(padx=30, pady=10)
        elif (task == 'quantize'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            quantizeBtn = Button(window, text='Quantizate', bg=foreColor, fg='white',
                                 width=150, font=('Arial', 15), command=lambda: quantize(window, quantizeBtn))
            quantizeBtn.pack(padx=30, pady=10)
        elif (task == 'dft'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            dftBtn = Button(window, text='DFT', bg=foreColor, fg='white',
                            width=150, font=('Arial', 15), command=lambda: DFT(window, dftBtn))
            dftBtn.pack(padx=30, pady=10)
        elif (task == 'idft'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            idftBtn = Button(window, text='IDFT', bg=foreColor, fg='white',
                             width=150, font=('Arial', 15), command=lambda: IDFT(window, idftBtn))
            idftBtn.pack(padx=30, pady=10)
        elif (task == 'dct'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            dctBtn = Button(window, text='DCT', bg=foreColor, fg='white',
                            width=150, font=('Arial', 15), command=lambda: dct(window, dctBtn))
            dctBtn.pack(padx=30, pady=10)
            getter_frame = tk.Frame(window, bg=mainColor)
            Label = tk.Label(getter_frame, text='Num of Coeffiecents',
                             font=('Arial', 15), bg=mainColor)
            Label.grid(row=0,column=0)
            global num_tbox
            num_tbox = tk.Entry(getter_frame)
            num_tbox.grid(row=0,column=1)
            getter_frame.pack()
        elif (task == 'dc'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            dcBtn = Button(window, text='Remove DC Component', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: remove_DC_component(window, dcBtn))
            dcBtn.pack(padx=30, pady=10)
        elif (task == 'smooth'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            smoothBtn = Button(window, text='Smoothing', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: smooth(window, smoothBtn))
            smoothBtn.pack(padx=30, pady=10)
        elif (task == 'sharp'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            sharpBtn = Button(window, text='Sharpening', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: sharp(window, sharpBtn))
            sharpBtn.pack(padx=30, pady=10)
        elif (task == 'fold'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            foldBtn = Button(window, text='Folding', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: fold(window, foldBtn))
            foldBtn.pack(padx=30, pady=10)
        elif (task == 'delay'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            delayBtn = Button(window, text='Delaying', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: delay(window, delayBtn))
            delayBtn.pack(padx=30, pady=10)
        elif (task == 'fold_shift'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            foldshiftBtn = Button(window, text='Fold -- Shift', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: fold_shift(window, foldshiftBtn))
            foldshiftBtn.pack(padx=30, pady=10)
        elif (task == 'remove_dc_freq'):
            displaySignals(window, fig, fig2)
            samples1 = samples
            dcBtn = Button(window, text='Remove DC Component', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15), command=lambda: remove_DC_in_freq(window, dcBtn))
            dcBtn.pack(padx=30, pady=10)
  

def add(window, Btn):
    global samples1, samples2
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    amplitudes2 = [sample[1] for sample in samples2[:-1]]
    sumAmlitudes = [0 for i in range(len(indecies))]

    for i in range(len(indecies)):
        sumAmlitudes[i] = amplitudes1[i] + amplitudes2[i]
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, sumAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, sumAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window,background=mainColor)
    Label = tk.Label(Frame, text='Signal#1+Signal#2', font=('Arial', 25),background=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    samples1 = []
    samples2 = []
    print('Checking Adding Test cases:')
    print('---------------------------')
    print('Signal#1+Signal#2:')
    SignalSamplesAreEqual(
        'Task 2/output signals/Signal1+signal2.txt', indecies, sumAmlitudes)
    print('Signal#1+Signal#3:')
    SignalSamplesAreEqual(
        'Task 2/output signals/signal1+signal3.txt', indecies, sumAmlitudes)
    print('--------------------------------------------------')


def Subtractor():
    root.deiconify()
    fourth_window = tk.Toplevel()
    fourth_window.configure(bg=mainColor)
    fourth_window.title("Subtractor")
    center_window(fourth_window, geometry_width, geometry_height)

    fourth_window.resizable(False, False)

    buildGettingTwoSignals(fourth_window, 'sub')
    createBackBtn(fourth_window)
    fourth_window.mainloop()


def sub(window, Btn):
    global samples1, samples2
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    amplitudes2 = [sample[1] for sample in samples2[:-1]]
    subAmlitudes = [0 for i in range(len(indecies))]

    for i in range(len(indecies)):
        subAmlitudes[i] = abs(amplitudes1[i] - amplitudes2[i])
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, subAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, subAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    samples1 = []
    samples2 = []
    Btn.destroy()
    Frame = tk.Frame(window, background=mainColor)
    Label = tk.Label(Frame, text='Signal#1-Signal#2', font=('Arial', 25),background=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking Subtraction Test cases:')
    print('--------------------------------')
    print('Signal#1-Signal#2:')
    SignalSamplesAreEqual(
        'Task 2/output signals/signal1-signal2.txt', indecies, subAmlitudes)
    print('Signal#1-Signal#3:')
    SignalSamplesAreEqual(
        'Task 2/output signals/signal1-signal3.txt', indecies, subAmlitudes)
    print('--------------------------------------------------')


def Multiplier():
    global constant_tbox
    root.deiconify()
    fifth_window = tk.Toplevel()
    center_window(fifth_window, geometry_width, geometry_height)

    fifth_window.resizable(False, False)
    fifth_window.configure(bg=mainColor)
    fifth_window.title("Multiplier")

    getterFrame = tk.Frame(fifth_window, bg=mainColor)
    getterFrame.pack(pady=10)

    constant_label = tk.Label(
        getterFrame, text="Constant", bg=mainColor, fg=foreColor, font=('Arial', 15))
    constant_label.grid(row=0, column=0)

    constant_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    constant_tbox.grid(row=0, column=1)

    signal_label = tk.Label(fifth_window, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(fifth_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(fifth_window, browseBtn, fifth_window, 'multiply'))
    browseBtn.pack(padx=30)

    createBackBtn(fifth_window)
    fifth_window.mainloop()


def multiply(window, Btn):
    global constant_tbox
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]

    multipliedAmlitudes = [0 for i in range(len(indecies))]

    constant = int(constant_tbox.get())

    for i in range(len(indecies)):
        multipliedAmlitudes[i] = amplitudes1[i] * constant
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, multipliedAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, multipliedAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Signal x ' + str(constant),
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking Subtraction Test cases:')
    print('--------------------------------')
    print('Signal#1 x 5:')
    SignalSamplesAreEqual(
        'Task 2/output signals/MultiplySignalByConstant-Signal1 - by 5.txt', indecies, multipliedAmlitudes)
    print('Signal#2 x 10:')
    SignalSamplesAreEqual(
        'Task 2/output signals/MultiplySignalByConstant-signal2 - by 10.txt', indecies, multipliedAmlitudes)
    print('--------------------------------------------------')


def Squaring():
    root.deiconify()
    sixth_window = tk.Toplevel()
    center_window(sixth_window, geometry_width, geometry_height)

    sixth_window.resizable(False, False)
    sixth_window.configure(bg=mainColor)
    sixth_window.title("Squaring")

    main_frame = tk.Frame(sixth_window, bg=mainColor)
    main_frame.pack(pady=25)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'square'))
    browseBtn.pack(padx=30, )

    createBackBtn(sixth_window)
    sixth_window.mainloop()


def square(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]

    squaredAmlitudes = [0 for i in range(len(indecies))]

    for i in range(len(indecies)):
        squaredAmlitudes[i] = amplitudes1[i] ** 2
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, squaredAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, squaredAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Signal ^2', font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking Subtraction Test cases:')
    print('--------------------------------')
    print('Signal#1 ^2:')
    SignalSamplesAreEqual(
        'Task 2/output signals/Output squaring signal 1.txt', indecies, squaredAmlitudes)
    print('--------------------------------------------------')


def Shifting():
    global shiftvalue_tbox
    root.deiconify()
    seventh_window = tk.Toplevel()
    center_window(seventh_window, geometry_width, geometry_height)
    seventh_window.resizable(False, False)
    seventh_window.configure(bg=mainColor)
    seventh_window.title("Shifting")

    getterFrame = tk.Frame(seventh_window, bg=mainColor)
    getterFrame.pack(pady=10)

    shiftvalue_label = tk.Label(
        getterFrame, text="Shift Value", bg=mainColor, fg=foreColor, font=('Arial', 15))
    shiftvalue_label.grid(row=0, column=0)

    shiftvalue_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    shiftvalue_tbox.grid(row=0, column=1)

    signal_label = tk.Label(seventh_window, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(seventh_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(seventh_window, browseBtn, seventh_window, 'shift'))
    browseBtn.pack(padx=30)

    createBackBtn(seventh_window)
    seventh_window.mainloop()


def shift(window, Btn):
    global shiftvalue_tbox
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    shiftedIndecies = [0 for i in range(len(indecies))]
    shiftvalue = int(shiftvalue_tbox.get())

    for i in range(len(indecies)):
        shiftedIndecies[i] = indecies[i] - shiftvalue

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(shiftedIndecies, amplitudes1)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(shiftedIndecies, amplitudes1)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Signal by shifting ' +
                                 str(shiftvalue), font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking shifting Test cases:')
    print('-----------------------------')
    print('Signal#1 add 500:')
    SignalSamplesAreEqual(
        'Task 2/output signals/output shifting by add 500.txt', shiftedIndecies, amplitudes1)
    print('Signal#2 minus 500:')
    SignalSamplesAreEqual(
        'Task 2/output signals/output shifting by minus 500.txt', shiftedIndecies, amplitudes1)
    print('--------------------------------------------------')


def Normalization():
    global minvalue_tbox
    global maxvalue_tbox
    root.deiconify()
    eighth_window = tk.Toplevel()
    center_window(eighth_window, geometry_width, geometry_height)
    eighth_window.resizable(False, False)
    eighth_window.configure(bg=mainColor)
    eighth_window.title("Normalization")
    getterFrame = tk.Frame(eighth_window, bg=mainColor)
    getterFrame.pack(pady=10)

    minvalue_label = tk.Label(
        getterFrame, text="Min Value", bg=mainColor, fg=foreColor, font=('Arial', 15))
    minvalue_label.grid(row=0, column=0)

    minvalue_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    minvalue_tbox.grid(row=0, column=1)

    maxvalue_label = tk.Label(
        getterFrame, text="Max Value", bg=mainColor, fg=foreColor, font=('Arial', 15))
    maxvalue_label.grid(row=1, column=0)

    maxvalue_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    maxvalue_tbox.grid(row=1, column=1)
    signal_label = tk.Label(eighth_window, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(eighth_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(eighth_window, browseBtn, eighth_window, 'normalize'))
    browseBtn.pack(padx=30)

    createBackBtn(eighth_window)
    eighth_window.mainloop()


def normalize(window, Btn):
    global minvalue_tbox
    global maxvalue_tbox

    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    normalizeAmlitudes = [0.0 for i in range(len(indecies))]
    minvalue = int(minvalue_tbox.get())
    maxvalue = int(maxvalue_tbox.get())
    for i in range(len(indecies)):
        normalizeAmlitudes[i] = (maxvalue - minvalue) * ((amplitudes1[i] - min(
            amplitudes1)) / (max(amplitudes1) - min(amplitudes1))) + minvalue

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, normalizeAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, normalizeAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Normalized Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking normalize Test cases:')
    print('--------------------------------')
    print('Signal#1 :')
    SignalSamplesAreEqual(
        'Task 2/output signals/normalize of signal 1 -- output.txt', indecies, normalizeAmlitudes)
    print('Signal#2 :')
    SignalSamplesAreEqual(
        'Task 2/output signals/normlize signal 2 -- output.txt', indecies, normalizeAmlitudes)
    print('--------------------------------------------------')


def Accumalator():
    root.deiconify()
    ninth_window = tk.Toplevel()
    center_window(ninth_window, geometry_width, geometry_height)
    ninth_window.resizable(False, False)
    ninth_window.configure(bg=mainColor)
    ninth_window.title("Accumalator")

    main_frame = tk.Frame(ninth_window, bg=mainColor)
    main_frame.pack(pady=25)
    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()
    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'accum'))
    browseBtn.pack(padx=30, )
    createBackBtn(ninth_window)
    ninth_window.mainloop()


def accum(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    accumAmlitudes = [0 for i in range(len(indecies))]
    res = 0.0
    output_list = []
    output_list.append(amplitudes1[0])
    for i in range(1, len(indecies)):
        res = output_list[i - 1]
        accumAmlitudes[i] = amplitudes1[i] + res
        output_list.append(accumAmlitudes[i])
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, accumAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, accumAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Accumlated Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking Accumlator Test cases:')
    print('--------------------------------')
    print('Signal#1 :')
    SignalSamplesAreEqual(
        'Task 2/output signals/output accumulation for signal1.txt', indecies, accumAmlitudes)
    print('--------------------------------------------------')


# Task::3
def QuantizationTest1(file_name, Your_EncodedValues, Your_QuantizedValues):
    expectedEncodedValues = []
    expectedQuantizedValues = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V2 = str(L[0])
                V3 = float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if ((len(Your_EncodedValues) != len(expectedEncodedValues)) or (
            len(Your_QuantizedValues) != len(expectedQuantizedValues))):
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_EncodedValues)):
        if (Your_EncodedValues[i] != expectedEncodedValues[i]):
            print(
                "QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one")
            return
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print(
                "QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one")
            return
    print("QuantizationTest1 Test case passed successfully")


def QuantizationTest2(file_name, Your_IntervalIndices, Your_EncodedValues, Your_QuantizedValues, Your_SampledError):
    expectedIntervalIndices = []
    expectedEncodedValues = []
    expectedQuantizedValues = []
    expectedSampledError = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 4:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = str(L[1])
                V3 = float(L[2])
                V4 = float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if (len(Your_IntervalIndices) != len(expectedIntervalIndices)
            or len(Your_EncodedValues) != len(expectedEncodedValues)
            or len(Your_QuantizedValues) != len(expectedQuantizedValues)
            or len(Your_SampledError) != len(expectedSampledError)):
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_IntervalIndices)):
        if (Your_IntervalIndices[i] != expectedIntervalIndices[i]):
            print(
                "QuantizationTest2 Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(Your_EncodedValues)):
        if (Your_EncodedValues[i] != expectedEncodedValues[i]):
            print(
                "QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one")
            return

    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print(
                "QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one")
            return
    for i in range(len(expectedSampledError)):
        if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one")
            return
    print("QuantizationTest2 Test case passed successfully")


def decimal_to_binary(decimal, num_bits):
    binary = format(decimal, '0{}b'.format(num_bits))
    return binary


def QuantizationAndEncoding():
    global var
    global levelsOrBits_tbox
    root.deiconify()
    tenth_window = tk.Toplevel()
    center_window(tenth_window, geometry_width, geometry_height)
    tenth_window.resizable(False, False)
    tenth_window.configure(bg=mainColor)
    tenth_window.title("QuantizationAndEncoding")
    getterFrame = tk.Frame(tenth_window, bg=mainColor)
    getterFrame.pack(pady=10)

    var = tk.StringVar()

    bits_radio = tk.Radiobutton(
        getterFrame, text="bit", variable=var, value='bit', bg=mainColor)
    levels_radio = tk.Radiobutton(
        getterFrame, text="level", variable=var, value='level', bg=mainColor)

    var.set('bit')

    bits_radio.grid(row=0, column=0)
    levels_radio.grid(row=0, column=1)

    label2 = tk.Label(getterFrame, text="Target", bg=mainColor, fg=foreColor)
    label2.grid(row=1, column=0)
    levelsOrBits_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    levelsOrBits_tbox.grid(row=1, column=1)

    signal_label = tk.Label(tenth_window, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()
    browseBtn = Button(tenth_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(tenth_window, browseBtn, tenth_window, 'quantize'))
    browseBtn.pack(padx=30, )

    createBackBtn(tenth_window)
    tenth_window.mainloop()


def quantize(window, Btn):
    global levelsOrBits_tbox
    global var
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes = [sample[1] for sample in samples1[:-1]]

    levelsnum = 0
    bitsnum = 0
    # Step::1
    min_value = min(amplitudes)  # 0.2
    max_value = max(amplitudes)  # 1
    # Step::2
    if (str(var.get()) == 'bit'):
        bitsnum = int(levelsOrBits_tbox.get())  # 3
        levelsnum = 2 ** bitsnum  # 8
    elif (str(var.get()) == 'level'):
        levelsnum = int(levelsOrBits_tbox.get())
        bitsnum = int(math.log(levelsnum, 2))
    delta = ((max_value - min_value) / levelsnum)  # 0.1
    # Step::3
    Intervals = []
    tmp = min_value
    for i in range(levelsnum):
        current = tmp
        nextval = current + delta
        Intervals.append((round(current, 2), round(nextval, 2)))
        tmp = tmp + delta
        if (tmp == max_value):
            break
    # Step::4
    mid_points = []
    for i in range(len(Intervals)):
        mid_points.append(round(((Intervals[i][0] + Intervals[i][1]) / 2), 2))
    # Step::5
    quantized_amp = []
    quantized_index = []
    Interval_Indecies = []
    for a in amplitudes:
        for i in range(len(Intervals)):
            if (a >= Intervals[i][0] and a <= Intervals[i][1]):
                quantized_amp.append(mid_points[i])
                quantized_index.append(i)
                Interval_Indecies.append(i + 1)
                break
    error_list = []
    error_list_squared = []

    for i in range(len(quantized_amp)):
        error_list.append(round((quantized_amp[i] - amplitudes[i]), 5))
        error_list_squared.append(error_list[i] ** 2)
    encoded_values = []
    for i in range(len(quantized_index)):
        encoded_values.append(decimal_to_binary(quantized_index[i], bitsnum))

    if (str(var.get()) == 'bit'):
        QuantizationTest1("Task 3 Test Cases/Test 1/Quan1_Out.txt",
                          encoded_values, quantized_amp)

    if (str(var.get()) == 'level'):
        QuantizationTest2("Task 3 Test Cases/Test 2/Quan2_Out.txt", Interval_Indecies,
                          encoded_values, quantized_amp, error_list)

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, quantized_amp)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, quantized_amp)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Output_frame = tk.Frame(window, bg=mainColor)
    Frame = tk.Frame(Output_frame, bg=mainColor)
    Label = tk.Label(Frame, text='Quantized Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)

    canvas = FigureCanvasTkAgg(fig, master=Frame)
    canvas.get_tk_widget().pack()
    Frame.grid(row=0, column=0, padx=30)

    tree = ttk.Treeview(Output_frame)

    tree["columns"] = ("Encoding", "X(n)", "Xq(n)", "error")

    tree.heading("#0", text="ID")
    tree.heading("Encoding", text="Encoding")
    tree.heading("X(n)", text="X(n)")
    tree.heading("Xq(n)", text="Xq(n)")
    tree.heading("error", text="error")

    tree.column("#0", width=80)
    tree.column("Encoding", width=100)
    tree.column("X(n)", width=100)
    tree.column("Xq(n)", width=100)
    tree.column("error", width=100)

    for i in range(len(quantized_index)):
        tree.insert("", "end", text=str(i), values=(
            encoded_values[i], amplitudes[i], quantized_amp[i], error_list[i]))

    tree.grid(row=0, column=1, padx=30)
    Output_frame.pack(padx=10)


# Task::4
def DiscreteFourierTransform():
    global frequency_tbox
    root.deiconify()
    elev_window = tk.Toplevel()
    center_window(elev_window, geometry_width, geometry_height)
    elev_window.resizable(False, False)
    elev_window.configure(bg=mainColor)
    elev_window.title("DiscreteFourierTransform")
    getterFrame = tk.Frame(elev_window, bg=mainColor)
    getterFrame.pack(pady=10)
    frequency_label = tk.Label(
        getterFrame, text="Sampling frequency", bg=mainColor, fg=foreColor, font=('Arial', 15))
    frequency_label.grid(row=0, column=0)
    frequency_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    frequency_tbox.grid(row=0, column=1)
    signal_label = tk.Label(elev_window, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(elev_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(elev_window, browseBtn, elev_window, 'dft'))
    browseBtn.pack(padx=30)
    createBackBtn(elev_window)
    elev_window.mainloop()


def SignalComapreAmplitude(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalInput):
        print('case 1 exit')
        return False
    else:
        for i in range(len(SignalInput)):
            A = round(SignalInput[i])
            B = round(SignalOutput[i])
            if abs(SignalInput[i] - SignalOutput[i]) > 0.001:
                return False
            elif A != B:
                return False
        return True


def SignalComaprePhaseShift(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        for i in range(len(SignalInput)):
            A = round(SignalInput[i])
            B = round(SignalOutput[i])
            if abs(A - B) > 0.0001:
                return False
            elif A != B:
                return False
        return True


def get_samples_only(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    samples = []

    for line in lines[3:]:
        values = line.strip().split()
        if ('f' in values[0]):
            values[0] = float(values[0].replace('f', ''))
        if ('f' in values[1]):
            values[1] = float(values[1].replace('f', ''))
        amplitude = float(values[0])
        phase = float(values[1])
        samples.append((amplitude, phase))
    return samples


def show_DFT(freq_List, ampli_List, Phase_List, window, Btn):
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Digital representation')
    # freq_List vs ampli_List
    ax.stem(freq_List, ampli_List)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Amplitude')
    # freq_List vs Phase_List
    ax2.stem(freq_List, Phase_List)
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Phase Shift')
    if (Btn != ''):
        Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='DFT Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)

    global Old_DFT_show
    Old_DFT_show = Frame


def DFT(window, Btn):
    global frequency_tbox

    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    sampling_frequency = int(frequency_tbox.get())

    # full float length for output txt file
    actual_Phase_List = []
    actual_ampli_List = []
    # only first 2 digits for plotting
    Phase_List = []
    freq_List = []
    ampli_List = []
    Omega = (2 * math.pi * sampling_frequency) / len(amplitudes1)

    for i in range(len(amplitudes1)):
        Amplitude = 0
        Phase = 0
        Freq_Value = 0.0

        complex_value = complex(0, 0)

        Freq_Value = Omega * (i + 1)

        for j in range(len(amplitudes1)):
            pi_value = ((-2 * math.pi * i * j) / len(amplitudes1))
            real = cmath.cos(pi_value)
            imaginary = cmath.sin(pi_value)
            number = complex(real, imaginary)
            complex_value = complex_value + (amplitudes1[j] * number)

            Amplitude = abs(complex_value)
            Phase = cmath.phase(complex_value)

        ampli_List.append(float(f"{float(Amplitude):.2f}"))
        Phase_List.append(float(f"{float(Phase):.2f}"))
        freq_List.append(f"{float(Freq_Value):.2f}")

        actual_ampli_List.append(float(f"{float(Amplitude):.14f}"))
        actual_Phase_List.append(float(f"{float(Phase):.14f}"))

    show_DFT(freq_List, ampli_List, Phase_List, window, Btn)

    # Test Cases checking:
    real_samples = get_samples_only(
        'Task 4 Test Cases/DFT/Output_Signal_DFT_A,Phase.txt')
    real_amplitudes = [sample[0] for sample in real_samples]
    real_phases = [sample[1] for sample in real_samples]

    checkAmp = SignalComapreAmplitude(real_amplitudes, actual_ampli_List)
    checkPhase = SignalComaprePhaseShift(real_phases, actual_Phase_List)

    if (checkAmp and checkPhase):
        print('DFT Test Cases Passed Sucessfully !')
    else:
        print('DFT Test Cases Failed !')

    # Saving the output into a text file:
    filename1 = "Task 4 Output/Output.txt"
    ampli_phase_list = ''
    for i in range(len(actual_Phase_List)):
        ampli_phase_list += str(actual_ampli_List[i]) + \
                            ' ' + str(actual_Phase_List[i]) + '\n'

    with open(filename1, "w") as file:
        to_be_saved = '0\n1\n' + str(len(amplitudes1)) + '\n' + ampli_phase_list
        file.write(to_be_saved)


def toggle():
    global btnandgetterFrame
    global varCheck
    global idftBtn
    if varCheck.get() == 1:
        btnandgetterFrame.pack()
        idftBtn.pack_forget()
    else:
        btnandgetterFrame.pack_forget()
        idftBtn.pack()


def Modify(window, idftBtn, freq, amplitudes, phases, btnandgetterFrame, check_box):
    freq_index = index_combo.get()
    newAmplitude = float(amp_tbox.get())
    newPhase = float(phase_tbox.get())
    index = freq.index(freq_index)
    amplitudes[index] = newAmplitude
    phases[index] = newPhase
    Old_DFT_show.destroy()
    show_DFT(freq, amplitudes, phases, window, '')
    btnandgetterFrame.destroy()
    check_box.destroy()
    idftBtn.pack()


def get_DFT(window, Btn):
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if filename:
        with open(filename, 'r') as file:
            lines = file.readlines()

        amplitudes = []
        phases = []

        for line in lines[3:]:
            values = line.strip().split(',')
            if ('f' in values[0]):
                values[0] = float(values[0].replace('f', ''))
            if ('f' in values[1]):
                values[1] = float(values[1].replace('f', ''))

            amplitude = float(values[0])
            phase = float(values[1])
            amplitudes.append(amplitude)
            phases.append(phase)
        freq = np.arange(1, len(amplitudes) + 1)
        freq = [str(label) + 'Ω' for label in freq]

        show_DFT(freq, amplitudes, phases, window, Btn)

        global varCheck
        varCheck = tk.IntVar()

        global check_box
        check_box = tk.Checkbutton(window, text="Modify ?", command=toggle,
                                   variable=varCheck, onvalue=1, offvalue=0, background='gold')
        check_box.pack()
        global btnandgetterFrame
        btnandgetterFrame = tk.Frame(window, background=mainColor)

        getterFrame = tk.Frame(btnandgetterFrame, background=mainColor)

        get1 = tk.Frame(getterFrame, background=mainColor)

        label1 = tk.Label(get1, text='index', background=mainColor)
        label1.grid(row=0, column=0)
        global index_combo
        index_combo = ttk.Combobox(get1, state="readonly", values=freq)
        index_combo.grid(row=0, column=1)

        get1.grid(row=0, column=0)

        get2 = tk.Frame(getterFrame, background=mainColor)

        label2 = tk.Label(get2, text='Amplitude', background=mainColor)
        label2.grid(row=0, column=0)
        global amp_tbox
        amp_tbox = ttk.Entry(get2, )
        amp_tbox.grid(row=0, column=1)

        get2.grid(row=0, column=1)

        get3 = tk.Frame(getterFrame, background=mainColor)

        label3 = tk.Label(get3, text='Phase shift', background=mainColor)
        label3.grid(row=0, column=0)
        global phase_tbox
        phase_tbox = ttk.Entry(get3, )
        phase_tbox.grid(row=0, column=1)

        get3.grid(row=0, column=2)

        getterFrame.pack()

        modifyBtn = Button(btnandgetterFrame, text='Modify', bg=foreColor, fg='white',
                           width=150, font=('Arial', 15),
                           command=lambda: Modify(window, idftBtn, freq, amplitudes, phases, btnandgetterFrame,
                                                  check_box))

        modifyBtn.pack()

        global idftBtn
        idftBtn = Button(window, text='IDFT', bg=foreColor, fg='white',
                         width=150, font=('Arial', 15),
                         command=lambda: IDFT(window, idftBtn, varCheck, freq, amplitudes, phases))

        idftBtn.pack()

        window.mainloop()


def IDFT(window, Btn, varCheck, freq, amplitudes, phases):
    global index_combo
    global phase_tbox
    global amp_tbox

    Btn.destroy()

    Real = 0
    Imaginary = 0
    Complex_Num = []
    time_domain_amplitudes = []
    for i in range(len(freq)):
        Real = amplitudes[i] * math.cos(phases[i])
        Imaginary = amplitudes[i] * math.sin(phases[i])
        number = complex(Real, Imaginary)
        Complex_Num.append(number)

    for i in range(len(freq)):
        complex_value = complex(0, 0)
        for j in range(len(freq)):
            pi_value = (2 * math.pi * j * i) / len(freq)
            real_value = math.cos(pi_value)
            imaginary_value = math.sin(pi_value)
            num = complex(real_value, imaginary_value)
            complex_value = complex_value + (Complex_Num[j] * num)
        time_domain_amplitudes.append(float(complex_value.real / len(freq)))

    time_domain_amplitudes = [int(round(amplitude)) for amplitude in time_domain_amplitudes]
    indecies = [i for i in range(len(time_domain_amplitudes))]

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, time_domain_amplitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, time_domain_amplitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='IDFT Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)

    # Test Cases checking:
    real_samples = get_samples_only(
        'Task 4 Test Cases/IDFT/Output_Signal_IDFT.txt')
    real_amplitudes = [sample[1] for sample in real_samples]
    if (SignalComapreAmplitude(time_domain_amplitudes, real_amplitudes)):
        print('IDFT Test Case Passed sucessfully !')
    else:
        print('IDFT Test Case Failed !')


def InverseDiscreteFourierTransform():
    root.deiconify()
    elev_window = tk.Toplevel()
    center_window(elev_window, geometry_width, geometry_height)
    elev_window.resizable(False, False)
    elev_window.configure(bg=mainColor)
    elev_window.title("Inverse Discrete Fourier Transform")

    browseBtn = Button(elev_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: get_DFT(elev_window, browseBtn))
    browseBtn.pack(padx=30)
    elev_window.mainloop()


# Task 5
def DCT():
    root.deiconify()
    thirdteen_window = tk.Toplevel()
    center_window(thirdteen_window, geometry_width, geometry_height)
    thirdteen_window.resizable(False, False)
    thirdteen_window.configure(bg=mainColor)
    thirdteen_window.title("DCT")

    main_frame = tk.Frame(thirdteen_window, bg=mainColor)
    main_frame.pack(pady=25)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'dct'))
    browseBtn.pack(padx=30, )

    createBackBtn(thirdteen_window)
    thirdteen_window.mainloop()


def dct(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    global num_tbox

    num = int(num_tbox.get())

    outputIndecies = [0 for i in range(len(indecies))]
    outputAmlitudes = outputIndecies

    for k in range(len(indecies)):
        for n in range(len(indecies)):
            outputAmlitudes[k] += amplitudes1[n] * math.cos(
                (math.pi / (4 * len(amplitudes1))) * ((2 * n) - 1) * ((2 * k) - 1))
        outputAmlitudes[k] *= math.sqrt(2.0 / len(amplitudes1))

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, outputAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, outputAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='DCT Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking DCT Test cases:')
    print('------------------------')
    SignalSamplesAreEqual(
        'Task 5/DCT/DCT_output.txt', outputIndecies, outputAmlitudes)
    print('--------------------------------------------------')
    # Saving the output into a text file:
    filename1 = "Task 5 Output/Output.txt"
    index_ampli_list = ''
    for i in range(num):
        index_ampli_list += str(indecies[i]) + \
                            ' ' + str(outputAmlitudes[i]) + '\n'

    with open(filename1, "w") as file:
        to_be_saved = '0\n1\n' + str(num) + '\n' + index_ampli_list
        file.write(to_be_saved)


def remove_DC():
    root.deiconify()
    fourteen_window = tk.Toplevel()
    center_window(fourteen_window, geometry_width, geometry_height)
    fourteen_window.resizable(False, False)
    fourteen_window.configure(bg=mainColor)
    fourteen_window.title("Remove DC Component")

    main_frame = tk.Frame(fourteen_window, bg=mainColor)
    main_frame.pack(pady=25)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'dc'))
    browseBtn.pack(padx=30, )

    createBackBtn(fourteen_window)
    fourteen_window.mainloop()


def remove_DC_component(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    outputAmlitudes = [0 for i in range(len(indecies))]
    result = []
    average = sum(amplitudes1) / len(amplitudes1)
    for i in range(len(indecies)):
        result.append(amplitudes1[i] - average)
    outputAmlitudes = result

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, outputAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, outputAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='DC Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Remove DC Component Test cases:')
    print('----------------------------------------')
    SignalSamplesAreEqual("Task 5/Remove DC component/DC_component_output.txt", indecies, outputAmlitudes)
    print('--------------------------------------------------')
#Task 6
def Smoothing():
    global numofpoints_tbox
    root.deiconify()
    fiveteen_window = tk.Toplevel()
    center_window(fiveteen_window, geometry_width, geometry_height)
    fiveteen_window.resizable(False, False)
    fiveteen_window.configure(bg=mainColor)
    fiveteen_window.title("Smoothing")

    getterFrame = tk.Frame(fiveteen_window, bg=mainColor)
    getterFrame.pack(pady=10)

    numofpoints_label = tk.Label(
        getterFrame, text="Number of points", bg=mainColor, fg=foreColor, font=('Arial', 15))
    numofpoints_label.grid(row=0, column=0)

    numofpoints_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    numofpoints_tbox.grid(row=0, column=1)

    signal_label = tk.Label(fiveteen_window, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(fiveteen_window, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(fiveteen_window, browseBtn, fiveteen_window, 'smooth'))
    browseBtn.pack(padx=30)

    createBackBtn(fiveteen_window)
    fiveteen_window.mainloop()
def smooth(window,Btn):
    global numofpoints_tbox
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    output=[]
    movingaverageAmlitudes = [0 for i in range(len(indecies))]
    Average=0.0
    numofpoints = int(numofpoints_tbox.get())
    Average = (numofpoints - 1) / 2
    for i in range(int(Average), len(amplitudes1) -int(Average)):
        output.append(amplitudes1[i])
    movingaverageAmlitudes = output
    indecies = indecies[:len(movingaverageAmlitudes)]
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, movingaverageAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, movingaverageAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Moving Average',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Smoothing Test cases:')
    print('------------------------------')
    print('[1] Test#1: Smoothing Signal#1, Window Size = 3:')
    SignalSamplesAreEqual("Task 6 Test Cases/Moving Average/MovAvgTest1.txt", indecies, movingaverageAmlitudes)
    print()
    print('[2] Test#2: Smoothing Signal#2, Window Size = 5:')
    SignalSamplesAreEqual("Task 6 Test Cases/Moving Average/MovAvgTest2.txt", indecies, movingaverageAmlitudes)
    print('--------------------------------------------------')
    
    
def Sharpening():
    root.deiconify()
    sixteen_window = tk.Toplevel()
    center_window(sixteen_window, geometry_width, geometry_height)
    sixteen_window.resizable(False, False)
    sixteen_window.configure(bg=mainColor)
    sixteen_window.title("Sharpening")

    main_frame = tk.Frame(sixteen_window, bg=mainColor)
    main_frame.pack(pady=25)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'sharp'))
    browseBtn.pack(padx=30, )

    createBackBtn(sixteen_window)
    sixteen_window.mainloop()
    

def sharp(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    FirstDerivative = [0 for i in range(len(indecies))]
    SecondDerivative = [0 for i in range(len(indecies))]
    first=[]
    second=[]
    for n in range(len(amplitudes1) - 1):
        if n == 0:
            first.append(amplitudes1[n] - 0)
        else:
            first.append(amplitudes1[n] - amplitudes1[n - 1])
        if n == 0:
            second.append(amplitudes1[n + 1] - (2 * amplitudes1[n]))
        elif n == (len(amplitudes1) - 1):
            second.append(-(2 * amplitudes1[n]) + amplitudes1[n - 1])
        else:
            second.append(
                amplitudes1[n + 1] - (2 * amplitudes1[n]) + amplitudes1[n - 1])
    FirstDerivative=first
    SecondDerivative=second
    indecies = [i for i in range(len(amplitudes1)-1)]
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Digital representation')
    # discrete
    ax.stem(indecies,FirstDerivative)
    ax.set_xlabel('Index')
    ax.set_ylabel('FirstDerivative')
    # discrete
    ax2.stem(indecies, SecondDerivative)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('SecondDerivative')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Sharpening',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # given Test Case Checking:
    DerivativeSignal()
    
    return

def DerivativeSignal():
    InputSignal=[]
    for i in range(100):
        InputSignal.append(float(i+1))
    expectedOutput_first = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    expectedOutput_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    """
    Write your Code here:
    Start
    """
  
    first=[]
    second=[]
    for n in range(len(InputSignal) - 1):
        if n == 0:
            first.append(InputSignal[n] - 0)
        else:
            first.append(InputSignal[n] - InputSignal[n - 1])
        if n == 0:
            second.append(InputSignal[n + 1] - (2 * InputSignal[n]))
        elif n == (len(InputSignal) - 1):
            second.append(-(2 * InputSignal[n]) + InputSignal[n - 1])
        else:
            second.append(
                InputSignal[n + 1] - (2 * InputSignal[n]) + InputSignal[n - 1])
    FirstDrev=first
    SecondDrev=second
    
    """
    End
    """
    
    """
    Testing your Code
    """
    if( (len(FirstDrev)!=len(expectedOutput_first)) or (len(SecondDrev)!=len(expectedOutput_second))):
        print("mismatch in length") 
        return
    first=second=True
    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
            continue
        else:
            first=False
            print("1st derivative wrong")
            return
    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
            continue
        else:
            second=False
            print("2nd derivative wrong") 
            return
    if(first and second):
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")
    return
def Folding():
    root.deiconify()
    seventeen_window = tk.Toplevel()
    center_window(seventeen_window, geometry_width, geometry_height)
    seventeen_window.resizable(False, False)
    seventeen_window.configure(bg=mainColor)
    seventeen_window.title("Folding")

    main_frame = tk.Frame(seventeen_window, bg=mainColor)
    main_frame.pack(pady=25)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'fold'))
    browseBtn.pack(padx=30, )

    createBackBtn(seventeen_window)
    seventeen_window.mainloop()


def fold(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    FoldedAmplitudes= [0 for i in range(len(indecies))]
    index_list = []
    Output = []
    for i in range(len(amplitudes1)):
        Output_Signal = amplitudes1[len(amplitudes1) - 1 - i]
        Output.append(Output_Signal)
        Num = amplitudes1[i]
        index_list.append(Num)
    FoldedAmplitudes = (Output)
    

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies,FoldedAmplitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitudes')
    # continous
    ax2.plot(indecies, FoldedAmplitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Folding',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Folding Test cases:')
    print('----------------------------')
    SignalSamplesAreEqual("Task 6 Test Cases/Shifting and Folding/Output_fold.txt", indecies,FoldedAmplitudes)
    print('--------------------------------------------------')
def Delaying():
  global delayvalue_tbox
  root.deiconify()
  eightteen_window = tk.Toplevel()
  center_window(eightteen_window, geometry_width, geometry_height)
  eightteen_window.resizable(False, False)
  eightteen_window.configure(bg=mainColor)
  eightteen_window.title("Delaying")

  getterFrame = tk.Frame(eightteen_window, bg=mainColor)
  getterFrame.pack()

  delayvalue_label = tk.Label(
      getterFrame, text="Delay Value", bg=mainColor, fg=foreColor, font=('Arial', 15))
  delayvalue_label.grid(row=0, column=0)

  delayvalue_tbox = tk.Entry(getterFrame, font=(
      'Arial', 15), bg='white', fg='black', )
  delayvalue_tbox.grid(row=0, column=1)

  signal_label = tk.Label(eightteen_window, text="Signal",
                          bg=mainColor, fg=foreColor, font=('Arial', 15))
  signal_label.pack()

  browseBtn = Button(eightteen_window, text='Browse', bg=foreColor, fg='white',
                     width=150, font=('Arial', 15),
                     command=lambda: getSignal_destroyBtn(eightteen_window, browseBtn, eightteen_window, 'delay'))
  browseBtn.pack(padx=30)

  createBackBtn(eightteen_window)
  eightteen_window.mainloop()
  
def Shift_Fold_Signal(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Shift_Fold_Signal Test case failed, your signal have different values from the expected one") 
            return
    print("Shift_Fold_Signal Test case passed successfully")

def delay(window, Btn):
    global delayvalue_tbox
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    delayedIndecies = [0 for i in range(len(indecies))]
    delayvalue = int(delayvalue_tbox.get())

    for i in range(len(indecies)):
        delayedIndecies[i] = indecies[i] + delayvalue

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(delayedIndecies, amplitudes1)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(delayedIndecies, amplitudes1)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Signal by Delaying ' +
                                 str(delayvalue), font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking Fold Shift Test cases:')
    print('-------------------------------')
    print('Fold Shift Test#1')
    Shift_Fold_Signal(
      'Task 6 Test Cases/Shifting and Folding/Output_ShifFoldedby500.txt', delayedIndecies, amplitudes1)
    print('End Fold Shift Test#1')
    print()
    print('Fold Shift Test#2')
    Shift_Fold_Signal(
      'Task 6 Test Cases/Shifting and Folding/Output_ShiftFoldedby-500.txt', delayedIndecies, amplitudes1)
    print('End Fold Shift Test#2')
    print('--------------------------------------------------')
    
def fold_shift(window, Btn):
    global delayvalue_tbox
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    #Folding
    FoldedAmplitudes= []
    for i in range(len(amplitudes1)):
        Output_Signal = amplitudes1[len(amplitudes1) - 1 - i]
        FoldedAmplitudes.append(Output_Signal)

    delayedIndecies = [0 for i in range(len(indecies))]
    delayvalue = int(delayvalue_tbox.get())
    print(len(delayedIndecies),len(FoldedAmplitudes))
    
    #Delaying
    for i in range(len(indecies)):
        delayedIndecies[i] = indecies[i] + delayvalue

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(delayedIndecies, FoldedAmplitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(delayedIndecies, FoldedAmplitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='Folded Delayed Signal by ' +
                                 str(delayvalue), font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    print('Checking Fold Shift Test cases:')
    print('-------------------------------')
    print('Fold Shift Test#1')
    Shift_Fold_Signal(
      'Task 6 Test Cases/Shifting and Folding/Output_ShifFoldedby500.txt', delayedIndecies, FoldedAmplitudes)
    print('End Fold Shift Test#1')
    print()
    print('Fold Shift Test#2')
    Shift_Fold_Signal(
      'Task 6 Test Cases/Shifting and Folding/Output_ShiftFoldedby-500.txt', delayedIndecies, FoldedAmplitudes)
    print('End Fold Shift Test#2')
    print('--------------------------------------------------')
    
def Fold_Shifting():
    global delayvalue_tbox
    root.deiconify()
    nineteen_window = tk.Toplevel()
    center_window(nineteen_window, geometry_width, geometry_height)
    nineteen_window.resizable(False, False)
    nineteen_window.configure(bg=mainColor)
    nineteen_window.title("Fold Shifting")

    main_frame = tk.Frame(nineteen_window, bg=mainColor)
    main_frame.pack()
    
    getterFrame = tk.Frame(main_frame, bg=mainColor)
    getterFrame.pack()

    
    delayvalue_label = tk.Label(
        getterFrame, text="Delay Value", bg=mainColor, fg=foreColor, font=('Arial', 15))
    delayvalue_label.grid(row=0, column=0)

    delayvalue_tbox = tk.Entry(getterFrame, font=(
        'Arial', 15), bg='white', fg='black', )
    delayvalue_tbox.grid(row=0, column=1)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'fold_shift'))
    browseBtn.pack(padx=30,)

    createBackBtn(nineteen_window)
    nineteen_window.mainloop()
    
def remove_DC_freq():
    root.deiconify()
    twinty_window = tk.Toplevel()
    center_window(twinty_window, geometry_width, geometry_height)
    twinty_window.resizable(False, False)
    twinty_window.configure(bg=mainColor)
    twinty_window.title("Remove DC Component")

    main_frame = tk.Frame(twinty_window, bg=mainColor)
    main_frame.pack(pady=25)

    signal_label = tk.Label(main_frame, text="Signal",
                            bg=mainColor, fg=foreColor, font=('Arial', 15))
    signal_label.pack()

    browseBtn = Button(main_frame, text='Browse', bg=foreColor, fg='white',
                       width=150, font=('Arial', 15),
                       command=lambda: getSignal_destroyBtn(main_frame, browseBtn, main_frame, 'remove_dc_freq'))
    browseBtn.pack(padx=30, )

    createBackBtn(twinty_window)
    twinty_window.mainloop()
    
def remove_DC_in_freq(window, Btn):
    indecies = [sample[0] for sample in samples1[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    
    #DFT
    
    Phase_List = []
    ampli_List = []
    

    for i in range(len(amplitudes1)):
        Amplitude = 0
        Phase = 0

        complex_value = complex(0, 0)


        for j in range(len(amplitudes1)):
            pi_value = ((-2 * math.pi * i * j) / len(amplitudes1))
            real = cmath.cos(pi_value)
            imaginary = cmath.sin(pi_value)
            number = complex(real, imaginary)
            complex_value = complex_value + (amplitudes1[j] * number)

            Amplitude = abs(complex_value)
            Phase = cmath.phase(complex_value)


        ampli_List.append(float(f"{float(Amplitude):.14f}"))
        Phase_List.append(float(f"{float(Phase):.14f}"))
    #Make first sample is complex(0,0)
    complex_value = complex(0,0)
    ampli_List[0] = abs(complex_value)
    Phase_List[0] = cmath.phase(complex_value)
    
    #IDFT
    Real = 0
    Imaginary = 0
    Complex_Num = []
    time_domain_amplitudes = []
    for i in range(len(ampli_List)):
        Real = ampli_List[i] * math.cos(Phase_List[i])
        Imaginary = ampli_List[i] * math.sin(Phase_List[i])
        number = complex(Real, Imaginary)
        Complex_Num.append(number)

    for i in range(len(ampli_List)):
        complex_value = complex(0, 0)
        for j in range(len(ampli_List)):
            pi_value = (2 * math.pi * j * i) / len(ampli_List)
            real_value = math.cos(pi_value)
            imaginary_value = math.sin(pi_value)
            num = complex(real_value, imaginary_value)
            complex_value = complex_value + (Complex_Num[j] * num)
        time_domain_amplitudes.append(float(complex_value.real / len(ampli_List)))

    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(indecies, time_domain_amplitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(indecies, time_domain_amplitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    Btn.destroy()
    Frame = tk.Frame(window, bg=mainColor)
    Label = tk.Label(Frame, text='removed DC Signal',
                     font=('Arial', 15), bg=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Remove DC Component Test cases:')
    print('----------------------------------------')
    SignalSamplesAreEqual("Task 5/Remove DC component/DC_component_output.txt", indecies, time_domain_amplitudes)
    print('--------------------------------------------------')
#Task 7
def convolution():
    root.deiconify()
    twintyone_window = tk.Toplevel()
    twintyone_window.configure(bg=mainColor)
    twintyone_window.title("Convolution")
    center_window(twintyone_window, geometry_width, geometry_height)

    twintyone_window.resizable(False, False)

    buildGettingTwoSignals(twintyone_window, 'convolve')
    createBackBtn(twintyone_window)
    twintyone_window.mainloop()
def ConvTest(Your_indices,Your_samples): 
    """
    Test inputs
    InputIndicesSignal1 =[-2, -1, 0, 1]
    InputSamplesSignal1 = [1, 2, 1, 1 ]
    
    InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
    InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
    """
    
    expected_indices=[-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1 ]

    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Conv Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Conv Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal have different values from the expected one") 
            return
    print("Conv Test case passed successfully")
def convolve(window,Btn):
    global samples1, samples2
    indecies_of_x = [sample[0] for sample in samples1[:-1]]
    indecies_of_h = [sample[0] for sample in samples2[:-1]]
    x = [sample[1] for sample in samples1[:-1]]
    h = [sample[1] for sample in samples2[:-1]]
    # First ::: Balancing the indecies between x,h:
    new_indecies = [i for i in range(indecies_of_x[0]+indecies_of_h[0],indecies_of_x[-1]+indecies_of_h[-1]+1)]
    
    # Determining which signal is start:
    min_threshold = 0
    start_is_x = False
    start_is_h = False
    if min(indecies_of_x[0],indecies_of_h[0]) == indecies_of_x[0]:
        min_threshold = indecies_of_h[0]
        start_is_x = True
    else:
        min_threshold = indecies_of_x[0]
        start_is_h = True
    # Balancing Signals
    if start_is_x:
        for i in range(len(x)-1,len(new_indecies)):
            x.append(0.0)
        for i in range(indecies_of_x[0],indecies_of_h[0]):
            h = [0.0] + h
    if start_is_h:
        for i in range(len(h)-1,len(new_indecies)):
            h.append(0)
        for i in range(indecies_of_h[0],indecies_of_x[0]):
            x = [0.0] + x
    x.append(0.0)
    h.append(0.0)
    
    # Second ::: Convolution
    
    before_threshold = []
    after_threshold = []
    
    for n in range(len(new_indecies)):
        summation = 0
        for k in range(len(indecies_of_x)):
            x_multiply_h = x[k]*h[n-k]
            summation += x_multiply_h
        if new_indecies[n] < min_threshold:
            before_threshold.append(summation)
        else:
            after_threshold.append(summation)
    convolvedAmlitudes = after_threshold + before_threshold

                
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(new_indecies, convolvedAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(new_indecies, convolvedAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    samples1 = []
    samples2 = []
    Btn.destroy()
    Frame = tk.Frame(window,background=mainColor)
    Label = tk.Label(Frame, text='Convoluated Signal', font=('Arial', 25),background=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Convolution Test cases:')
    print('--------------------------------')
    ConvTest(new_indecies,convolvedAmlitudes)
    print('--------------------------------------------------')

    
# Task 8::
    
def Compare_Signals(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Correlation Test case failed, your signal have different values from the expected one") 
            return
    print("Correlation Test case passed successfully")


def correlating():
    
   root.deiconify()
   twintytwo_window = tk.Toplevel()
   twintytwo_window.configure(bg=mainColor)
   twintytwo_window.title("Correlation")
   center_window(twintytwo_window, geometry_width, geometry_height)

   twintytwo_window.resizable(False, False)

   buildGettingTwoSignals(twintytwo_window, 'correlate')
   createBackBtn(twintytwo_window)
   twintytwo_window.mainloop()
   
def correlation(window,Btn):
    global samples1, samples2
    indecies1 = [sample[0] for sample in samples1[:-1]]
    indecies2 = [sample[0] for sample in samples2[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    amplitudes2 = [sample[1] for sample in samples2[:-1]]
    
    is_periodic = samples2[-1]
     
    normCorrelatedAmplitudes = []
    N = len(indecies1)
    for i in range(N):
        # Sum of Products
        current_sum = 0
        for i in range(N):
            current_sum+=amplitudes1[i]*amplitudes2[i]
        corr = current_sum/N
        # Normaliztion
        sum_of_amplitudes1_squared = 0
        sum_of_amplitudes2_squared = 0
        for i in range(N):
            sum_of_amplitudes1_squared+=pow(amplitudes1[i], 2)
            sum_of_amplitudes2_squared+=pow(amplitudes2[i], 2)
        corr_norm = corr/(1/N * (math.sqrt(sum_of_amplitudes1_squared * sum_of_amplitudes2_squared)))
        normCorrelatedAmplitudes.append(corr_norm)
        # Shift right the signal
        first_value = amplitudes2[0]
        for i in range(len(amplitudes2)-1):
            amplitudes2[i] = amplitudes2[i+1]
        if(is_periodic==1):
            amplitudes2[-1] = first_value
        else:
            amplitudes2[-1] = 0
       
    outputIndecies = [i for i in range(len(normCorrelatedAmplitudes))]
    
    print(normCorrelatedAmplitudes)
    
    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(outputIndecies, normCorrelatedAmplitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(outputIndecies, normCorrelatedAmplitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    samples1 = []
    samples2 = []
    Btn.destroy()
    Frame = tk.Frame(window,background=mainColor)
    Label = tk.Label(Frame, text='Normalized Correlated Signal', font=('Arial', 25),background=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Correlation Test cases:')
    print('--------------------------------')
    Compare_Signals("Task 8 Test Cases/CorrOutput.txt",indecies1,normCorrelatedAmplitudes)
    print('--------------------------------------------------')


# Practical Task:::
def fast_convolution():
    
   root.deiconify()
   twintythree_window = tk.Toplevel()
   twintythree_window.configure(bg=mainColor)
   twintythree_window.title("Fast Convolution")
   center_window(twintythree_window, geometry_width, geometry_height)

   twintythree_window.resizable(False, False)

   buildGettingTwoSignals(twintythree_window, 'fast_convolve')
   createBackBtn(twintythree_window)
   twintythree_window.mainloop()

def fast_correlating():
    
   root.deiconify()
   twintyfour_window = tk.Toplevel()
   twintyfour_window.configure(bg=mainColor)
   twintyfour_window.title("Fast Correlation")
   center_window(twintyfour_window, geometry_width, geometry_height)

   twintyfour_window.resizable(False, False)

   buildGettingTwoSignals(twintyfour_window, 'fast_correlate')
   createBackBtn(twintyfour_window)
   twintyfour_window.mainloop()

def fast_convolve(window,Btn):
    global samples1, samples2
    indecies_of_x = [sample[0] for sample in samples1[:-1]]
    indecies_of_h = [sample[0] for sample in samples2[:-1]]
    x = [sample[1] for sample in samples1[:-1]]
    h = [sample[1] for sample in samples2[:-1]]
    appended_signal1=[]
    appended_signal2=[]
    new_indecies = []
    convolvedAmlitudes = []
    n1=len(x)
    n2=len(h)
    total=n1+n2-1
    appended_signal1 = x + [0.0] * (total - n1)
    appended_signal2 = h + [0.0] * (total - n2)

    
    Phase_Listx = []
    ampli_Listx = []
    for i in range(len(appended_signal1)):
        Amplitudex = 0
        Phasex = 0

        complex_valuex = complex(0, 0)

        for j in range(len(appended_signal1)):
            pi_valuex = ((-2 * math.pi * i * j) / len(appended_signal1))
            realx = cmath.cos(pi_valuex)
            imaginaryx = cmath.sin(pi_valuex)
            numberx = complex(realx, imaginaryx)
            complex_valuex = complex_valuex + (appended_signal1[j] * numberx)

            Amplitudex = abs(complex_valuex)
            Phasex = cmath.phase(complex_valuex)


        ampli_Listx.append(Amplitudex)
        Phase_Listx.append(Phasex)
    
    Phase_Listh = []
    ampli_Listh = []
    for i in range(len(appended_signal2)):
        Amplitudeh = 0
        Phaseh = 0

        complex_valueh = complex(0, 0)


        for j in range(len(appended_signal2)):
            pi_valueh = ((-2 * math.pi * i * j) / len(appended_signal2))
            realh = cmath.cos(pi_valueh)
            imaginaryh = cmath.sin(pi_valueh)
            numberh = complex(realh, imaginaryh)
            complex_valueh = complex_valueh + (appended_signal2[j] * numberh)

            Amplitudeh = abs(complex_valueh)
            Phaseh = cmath.phase(complex_valueh)


        ampli_Listh.append(Amplitudeh)
        Phase_Listh.append(Phaseh)
    
    result_amplitudes = []
    result_phases = []

    # Multiply amplitudes and add phases component-wise
    for i in range(len(ampli_Listx)):
        result_amplitude = ampli_Listx[i] * ampli_Listh[i]
        result_phase = Phase_Listx[i] + Phase_Listh[i]

        result_amplitudes.append(result_amplitude)
        result_phases.append(result_phase)

    #IDFT
    Real = 0
    Imaginary = 0
    Complex_Num = []
    time_domain_amplitudes = []
    for i in range(len(result_amplitudes)):
        Real = result_amplitudes[i] * math.cos(result_phases[i])
        Imaginary = result_amplitudes[i] * math.sin(result_phases[i])
        number = complex(Real, Imaginary)
        Complex_Num.append(number)

    for i in range(len(result_amplitudes)):
        complex_value = complex(0, 0)
        for j in range(len(result_amplitudes)):
            pi_value = (2 * math.pi * j * i) / len(result_amplitudes)
            real_value = math.cos(pi_value)
            imaginary_value = math.sin(pi_value)
            num = complex(real_value, imaginary_value)
            complex_value = complex_value + (Complex_Num[j] * num)
        time_domain_amplitudes.append(float(complex_value.real / len(result_amplitudes)))
    convolvedAmlitudes=time_domain_amplitudes
    
    
    new_indecies = [i for i in range(indecies_of_x[0]+indecies_of_h[0],indecies_of_x[-1]+indecies_of_h[-1]+1)]
    
    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(new_indecies, convolvedAmlitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(new_indecies, convolvedAmlitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')
    
    samples1 = []
    samples2 = []
    Btn.destroy()
    Frame = tk.Frame(window,background=mainColor)
    Label = tk.Label(Frame, text='Convoluted Signal', font=('Arial', 25),background=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    
    # Test Cases Checking:
    print('Checking Fast Convolution Test cases:')
    print('--------------------------------')
    ConvTest(new_indecies,convolvedAmlitudes)
    print('--------------------------------------------------')
    
def fast_correlation(window,Btn):
    global samples1, samples2
    indecies1 = [sample[0] for sample in samples1[:-1]]
    indecies2 = [sample[0] for sample in samples2[:-1]]
    amplitudes1 = [sample[1] for sample in samples1[:-1]]
    amplitudes2 = [sample[1] for sample in samples2[:-1]]
    
    outputIndecies = indecies1
    # Signal#1 DFT [x1*]
    Phase_List_signal1 = []
    ampli_List_signal1 = []
    for i in range(len(amplitudes1)):
        Amplitude = 0
        Phase = 0

        complex_value = complex(0, 0)


        for j in range(len(amplitudes1)):
            pi_value = ((-2 * math.pi * i * j) / len(amplitudes1))
            real = cmath.cos(pi_value)
            imaginary = -cmath.sin(pi_value) # - Imaginary part
            number = complex(real, imaginary)
            complex_value = complex_value + (amplitudes1[j] * number)

            Amplitude = abs(complex_value)
            Phase = cmath.phase(complex_value)


        ampli_List_signal1.append(Amplitude)
        Phase_List_signal1.append(Phase)
    
    # Signal#2 DFT [x2]
    Phase_List_signal2 = []
    ampli_List_signal2 = []
    for i in range(len(amplitudes2)):
        Amplitude = 0
        Phase = 0

        complex_value = complex(0, 0)


        for j in range(len(amplitudes2)):
            pi_value = ((-2 * math.pi * i * j) / len(amplitudes2))
            real = cmath.cos(pi_value)
            imaginary = cmath.sin(pi_value)
            number = complex(real, imaginary)
            complex_value = complex_value + (amplitudes2[j] * number)

            Amplitude = abs(complex_value)
            Phase = cmath.phase(complex_value)


        ampli_List_signal2.append(Amplitude)
        Phase_List_signal2.append(Phase)
    
    # Multiplication [(x1*) * (x2)]
    result_amplitudes = []
    result_phases = []
    for i in range(len(amplitudes1)):
        result_amplitude = ampli_List_signal1[i] * ampli_List_signal2[i]
        result_phase = Phase_List_signal1[i]+Phase_List_signal2[i]
        result_amplitudes.append(result_amplitude)
        result_phases.append(result_phase)
    
    
    # IDFT [FD^-1]
    Real = 0
    Imaginary = 0
    Complex_Num = []
    time_domain_amplitudes = []
    for i in range(len(result_amplitudes)):
        Real = result_amplitudes[i] * math.cos(result_phases[i])
        Imaginary = result_amplitudes[i] * math.sin(result_phases[i])
        number = complex(Real, Imaginary)
        Complex_Num.append(number)

    for i in range(len(result_amplitudes)):
        complex_value = complex(0, 0)
        for j in range(len(result_amplitudes)):
            pi_value = (2 * math.pi * j * i) / len(result_amplitudes)
            real_value = math.cos(pi_value)
            imaginary_value = math.sin(pi_value)
            num = complex(real_value, imaginary_value)
            complex_value = complex_value + (Complex_Num[j] * num)
        time_domain_amplitudes.append(float(complex_value.real / len(result_amplitudes)))
        
    correlatedAmplitudes = []
    
    for amp in time_domain_amplitudes:
        corr = amp/len(amplitudes1)
        correlatedAmplitudes.append(corr)
    
    
    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Digital representation')
    ax2.set_title('Analog representation')
    # discrete
    ax.stem(outputIndecies, correlatedAmplitudes)
    ax.set_xlabel('Index')
    ax.set_ylabel('Amplitude')
    # continous
    ax2.plot(outputIndecies, correlatedAmplitudes)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Amplitude')

    samples1 = []
    samples2 = []
    Btn.destroy()
    Frame = tk.Frame(window,background=mainColor)
    Label = tk.Label(Frame, text='Correlated Signal', font=('Arial', 25),background=mainColor)
    Label.pack(padx=10)
    displaySignals(Frame, fig, fig2)
    Frame.pack(padx=10)
    # Test Cases Checking:
    print('Checking Fast Correlation Test cases:')
    print('-------------------------------------')
    Compare_Signals("Task 9 Test Cases/Corr_Output.txt",indecies1,correlatedAmplitudes)
    print('--------------------------------------------------')


if __name__ == "__main__":
    root.configure(bg=mainColor)
    root.title("DSP Task")
    center_window(root, 588, 700)

    root.resizable(False, False)

    label = tk.Label(root, text="DSP Lab Practise", font=(
        'Arial', 25), bg='#FFDB58', fg=foreColor)
    label.pack(padx=25, pady=15)

    canvas = tk.Canvas(root, bg=mainColor)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL,
                             command=canvas.yview, bg=mainColor)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    button_area = tk.Frame(canvas, bg=mainColor)

    canvas.create_window((0, 0), window=button_area, anchor=tk.NW)

    # Read Signals
    firstbtn = Button(button_area, bg=foreColor, fg='white', text="Read samples & generate signals",
                      width=50, height=2, font=('Arial', 15), command=readSamples)
    firstbtn.pack(padx=2, pady=2)
    # Generate sin/cos signals
    secondbtn = Button(button_area, bg=foreColor, fg='white', text="Generate sinusoidal/cosinusoidal signals",
                       width=50, height=2, font=('Arial', 15), command=generateSinCosSignals)
    secondbtn.pack(padx=2, pady=2)
    # Adder
    thirdbtn = Button(button_area, bg=foreColor, fg='white', text="Add two signals",
                      width=50, height=2, font=('Arial', 15), command=Adder)
    thirdbtn.pack(padx=2, pady=2)
    # Subtractor
    fourthbtn = Button(button_area, bg=foreColor, fg='white', text="Subtract two signals",
                       width=50, height=2, font=('Arial', 15), command=Subtractor)
    fourthbtn.pack(padx=2, pady=2)
    # Multiplier
    fifthbtn = Button(button_area, bg=foreColor, fg='white', text="Multiply signal by constant",
                      width=50, height=2, font=('Arial', 15), command=Multiplier)
    fifthbtn.pack(padx=2, pady=2)
    # Squaring
    sixthbtn = Button(button_area, bg=foreColor, fg='white', text="Square a signal",
                      width=50, height=2, font=('Arial', 15), command=Squaring)
    sixthbtn.pack(padx=2, pady=2)
    # Shifting
    seventhbtn = Button(button_area, bg=foreColor, fg='white', text="Shift a signal",
                        width=50, height=2, font=('Arial', 15), command=Shifting)
    seventhbtn.pack(padx=2, pady=2)
    # Normalization
    eighthbtn = Button(button_area, bg=foreColor, fg='white', text="Normalize a signal",
                       width=50, height=2, font=('Arial', 15), command=Normalization)
    eighthbtn.pack(padx=2, pady=2)
    # Accumalatour
    ninththbtn = Button(button_area, bg=foreColor, fg='white', text="Accumalate a signal",
                        width=50, height=2, font=('Arial', 15), command=Accumalator)
    ninththbtn.pack(padx=2, pady=2)
    # Quantization
    tenthbtn = Button(button_area, bg=foreColor, fg='white', text="Quantization & Encoding",
                      width=50, height=2, font=('Arial', 15), command=QuantizationAndEncoding)
    tenthbtn.pack(padx=2, pady=2)
    # Discrete Fourier Transform
    elevbtn = Button(button_area, bg=foreColor, fg='white', text="Discrete Fourier Transform",
                     width=50, height=2, font=('Arial', 15), command=DiscreteFourierTransform)
    elevbtn.pack(padx=2, pady=2)
    # Inverse Discrete Fourier Transform
    twelvebtn = Button(button_area, bg=foreColor, fg='white', text="Inverse Discrete Fourier Transform ",
                       width=50, height=2, font=('Arial', 15), command=InverseDiscreteFourierTransform)
    twelvebtn.pack(padx=2, pady=2)
    # DCT
    thirdteenbtn = Button(button_area, bg=foreColor, fg='white', text="DCT",
                          width=50, height=2, font=('Arial', 15), command=DCT)
    thirdteenbtn.pack(padx=2, pady=2)
    # Remove DC Component
    fourteenbtn = Button(button_area, bg=foreColor, fg='white', text="Remove DC Component",
                         width=50, height=2, font=('Arial', 15), command=remove_DC)
    fourteenbtn.pack(padx=2, pady=2)
    #Smoothing
    fiveteenbtn = Button(button_area, bg=foreColor, fg='white', text="Smoothing",
                         width=50, height=2, font=('Arial', 15), command=Smoothing)
    fiveteenbtn.pack(padx=2, pady=2)
    #Sharpening
    sixteenbtn = Button(button_area, bg=foreColor, fg='white', text="Sharpening",
                         width=50, height=2, font=('Arial', 15), command=Sharpening)
    sixteenbtn.pack(padx=2, pady=2)
    #folding
    seventeenbtn = Button(button_area, bg=foreColor, fg='white', text="Folding",
                         width=50, height=2, font=('Arial', 15), command=Folding)
    seventeenbtn.pack(padx=2, pady=2)
    #Delaying
    eightteenbtn = Button(button_area, bg=foreColor, fg='white', text="Delaying",
                         width=50, height=2, font=('Arial', 15), command=Delaying)
    eightteenbtn.pack(padx=2, pady=2)
    # Remove DC Component in freq domain
    nineteenbtn = Button(button_area, bg=foreColor, fg='white', text="Fold Shifting",
                         width=50, height=2, font=('Arial', 15), command=Fold_Shifting)
    nineteenbtn.pack(padx=2, pady=2)
    # Remove DC Component in freq domain
    twintybtn = Button(button_area, bg=foreColor, fg='white', text="Remove DC Component in frequency domain",
                         width=50, height=2, font=('Arial', 15), command=remove_DC_freq)
    twintybtn.pack(padx=2, pady=2)
    # Convolution
    twintyonebtn = Button(button_area, bg=foreColor, fg='white', text="Convolution",
                         width=50, height=2, font=('Arial', 15), command=convolution)
    twintyonebtn.pack(padx=2, pady=2)
    # Correlation
    twintytwobtn = Button(button_area, bg=foreColor, fg='white', text="Correlation",
                         width=50, height=2, font=('Arial', 15), command=correlating)
    twintytwobtn.pack(padx=2, pady=2)
    # Fast Convolution
    twintythreebtn = Button(button_area, bg=foreColor, fg='white', text="Fast Convolution",
                         width=50, height=2, font=('Arial', 15), command=fast_convolution)
    twintythreebtn.pack(padx=2, pady=2)
    # Fast Correlation
    twintyfourbtn = Button(button_area, bg=foreColor, fg='white', text="Fast Correlation",
                         width=50, height=2, font=('Arial', 15), command=fast_correlating)
    twintyfourbtn.pack(padx=2, pady=2)


    canvas.configure(scrollregion=canvas.bbox("all"))

    root.mainloop()
