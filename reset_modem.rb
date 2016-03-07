#!/usr/bin/env ruby
require 'httparty'
begin
  HTTParty.post('http://192.168.100.1/goform/RgConfig', {:body => { "ResetReq" => 1 } })
rescue HTTParty::Error=>e
  puts "Error resetting modem: #{e}"
  exit
rescue StandardError=>e
  puts "Error resetting modem:  #{e}"
  exit
end
