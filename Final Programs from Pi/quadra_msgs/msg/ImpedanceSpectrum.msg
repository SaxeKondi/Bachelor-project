# A single Quadra measurement sample spectrum.

std_msgs/Header header
uint32 measurement_period  # Internally measured single-spectrum acquisition period [microseconds]
float32[15] frequency      # Spectrum frequency values [Hz]
float32[15] magnitude      # Impedance magnitude values [Ohm]
float32[15] phase          # Impedance phase values [degree]
