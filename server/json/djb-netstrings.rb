# See for detail of netstrings protocol:
#   http://cr.yp.to/proto/netstringss.txt

module DjbNetstrings
  BadStringError = Class.new(StandardError)
  InvalidDataLengthError = Class.new(BadStringError)
  LengthMismatchError = Class.new(BadStringError)
  UnterminatedStringError = Class.new(BadStringError)
  LengthLimitExceedError = Class.new(BadStringError)

  # 0 upto 99999999 bytes (96 MB)
  LENGTH_DIGITSNUM_RANGE = (1..8)

  class << self
    def fail_length_exceed(len, limit)
      raise(DjbNetstrings::LengthLimitExceedError,
            "Peer attempt to send data of #{len}B larger than #{limit}B.")
    end

    def ns_pack(str)
      str = str.to_s
      "#{str.size}:#{str},"
    end

    def ns_unpack(packed)
      packed.kind_of?(String) or raise(ArgumentError)

      (packed[-1] == ?,) or raise(DjbNetstrings::UnterminatedStringError.new(packed))
      return "" if packed[0] == ?0
      len, data = packed.split(":", 2)
      len = extract_length(len)
      ((data.size - 1) == len) or raise(DjbNetstrings::LengthMismatchError.new(packed))
      data[0...len]
    end

    def ns_read(io, limit = nil)
      len = io.readline(":")
      data = if len[0] == ?0
               ""
             else
               len.chop!
               len = extract_length(len)
               if limit && (len > limit)
                 fail_length_exceed(len, limit)
               end
               io.read(len)
             end
      (io.getc == ?,) or raise(DjbNetstrings::UnterminatedStringError.new(data))
      data
    end

    def ns_write(io, str)
      io << "#{str.size}:" << str << ","
      io.flush
    end

    def extract_length(len)
      (LENGTH_DIGITSNUM_RANGE === len.size) or
        raise(DjbNetstrings::InvalidDataLengthError)
      Integer(len) rescue raise(DjbNetstrings::InvalidDataLengthError)
    end
  end #/<< self
end #/DjbNetstrings
