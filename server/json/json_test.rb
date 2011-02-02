#! /usr/bin/env ruby
require 'rubygems'
require 'json'
require 'djb-netstrings'

f = ARGV[0] && File.open(ARGV[0], 'r') || $stdin
begin
  until f.eof?
    j = DjbNetstrings.ns_read(f)
    o = JSON.parse(j)
    puts JSON.pretty_generate(o)
    puts
    j = ''
  end
rescue Exception => e
  puts "Line #{f.lineno} (byte #{f.pos}) failed:\n#{e}\n#{j}"
end
