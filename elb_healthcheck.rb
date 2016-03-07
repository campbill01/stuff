#!/usr/bin/env ruby
#  script to test services from localhost (stack)
#  serve from nginx to elb for healthcheck
#  need to install httparty in bootconfig
# 
require 'httparty'
puts 'Content-type: text/html'
IPADDRESS=HTTParty.get('http://169.254.169.254/latest/meta-data/local-ipv4')
def error_exit(service='nginx')
	puts "Status: 500"
	puts "Error in #{service}"
    exit
end
# if nginx is not up, this healthcheck will not run so instance will be unhealthy
SERVICES={"events" => 8005, "security" => 8010, "service" => 8011, "email" => 8013, "warehouse" => 8012}
SERVICES.each do |key,service|
  begin 
    response=HTTParty.get("http://#{IPADDRESS}:#{service}/healthcheck")
    rescue HTTParty::Error=>e
    	error_exit(key)
    rescue StandardError=>e
    	error_exit(key)
    end 	
    if response.include? "false"
      error_exit(key)
    end
end
