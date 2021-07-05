#include <Arduino.h>

#include <math.h>
#include <PDM.h>

// #include <arduinoFFT.h>

// arduinoFFT fft = arduinoFFT();

/*
NOTE: set SERIAL_PLOT_MODE to false while creating FFT audio dataset
LED_BUILTIN will be on if upload the in Serial plot mode
*/
#define SERIAL_PLOT_MODE false
#define PDM_SOUND_GAIN 30 // sound gain of PDM mic
#define BUFFER_SIZE 256   // buffer size of PDM mic

#define SAMPLE_DELAY 8      // delay time (ms) between sampling
#define SAMPLING_FREQ 16000 // sampling frequency of on Board microphone
#define CHANNEL 1           // Number of Channel Microphone has

volatile float rms;

short sample_buffer[BUFFER_SIZE];
short feature_data[BUFFER_SIZE / 2];
// double vReal[BUFFER_SIZE];
// double vImaginary[BUFFER_SIZE];

// callback function for PDM mic
void onPDMdata()
{
  rms = -1;

  int bytes_available = PDM.available();
  PDM.read(sample_buffer, bytes_available);

  // calculate RMS (root mean square) from sample_buffer
  unsigned int sum = 0;
  for (unsigned short i = 0; i < (bytes_available / 2); i++)
    sum += pow(sample_buffer[i], 2);
  rms = sqrt(double(sum) / (double(bytes_available) / 2.0));
}

// Transfor Audio raw data from time domain to frquency domain
// double getAudiospectrum(double *vReal, double *vImaginary, unsigned int samples)
// {
//   fft.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
//   fft.Compute(vReal, vImaginary, samples, FFT_FORWARD);
//   fft.ComplexToMagnitude(vReal, vImaginary, samples);

//   return double(*vReal);
// }

void setup()
{

  Serial.begin(115200);
  while (!Serial)
    ;

  pinMode(LEDG, OUTPUT);
  pinMode(LEDG, OUTPUT);

  PDM.onReceive(onPDMdata);
  PDM.setBufferSize(BUFFER_SIZE);
  PDM.setGain(PDM_SOUND_GAIN);

  // Begin PDM
  if (!PDM.begin(CHANNEL, SAMPLING_FREQ))
  { // start PDM mic and sampling at 16 KHz
    Serial.println("Failed to start PDM!");
    while (1)
      ;
  }
}

void loop()
{
  if (SERIAL_PLOT_MODE)
  {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
  }

  while (Serial.available() > 0)
  {
    char command = Serial.read();
    if (command == '1')
    {

      delay(200);
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDG, LOW);
      for (unsigned short i = 0; i < BUFFER_SIZE / 2; i++)
      { // sampling
        while (rms < 0)
          ;
        feature_data[i] = rms;
        // vReal[i] = sample_buffer[i];
        // vImaginary[i] = 0.0;

        delay(SAMPLE_DELAY);
      }

      digitalWrite(LEDG, HIGH);

      // getAudiospectrum(vReal, vImaginary, BUFFER_SIZE);

      // samplesRead = 0;
      // pring out sampling data
      if (!SERIAL_PLOT_MODE)
      {
        Serial.print("[");
      }

      for (unsigned short i = 0; i < BUFFER_SIZE / 2; i++)
      {
        if (!SERIAL_PLOT_MODE)
        {
          Serial.print(feature_data[i]);
          Serial.print(", ");
        }
        else
        {
          Serial.println(feature_data[i]);
        }
      }
      if (!SERIAL_PLOT_MODE)
      {
        Serial.println("],");
      }
      else
      {
        for (unsigned short i = 0; i < (BUFFER_SIZE / 2); i++)
          Serial.println(0);
      }
    }
  }
}