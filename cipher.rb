class Deck_of_cards
  def initialize
    #define cards
    @cards=[]
    suits=['clubs','diamonds','hearts','spades']
    suits.each do |suit|
      @cards.push("#{suit}.ace")
      (2..10).each do |num|
        @cards.push("#{suit}.#{num}")                        
      end
    @cards.push("#{suit}.jack")
    @cards.push("#{suit}.queen")
    @cards.push("#{suit}.king")
    end
    @cards.push("joker.A")
    @cards.push("joker.B")
    end # end initialize
  def shuffle
    # actually prepare the deck for encryption
    move_joker('joker.A')
    move_joker('joker.B')
    triple_cut
    count_cut
  end
  
  def count_cut
    size=get_value(@cards[53],'card')
    lower=@cards.slice!(53,53)
    count_array=@cards.slice!(0,size)
    @cards=@cards + count_array + lower
    end
  def find_output
    shuffle
    #puts "finding output letter value"
    count=get_value(@cards[0],'card')
    letter_card=@cards[count]
    pre_number=get_value(letter_card,'card')
      if pre_number < 27
        output=get_return(pre_number)
      else
        output=get_return(pre_number -26)
      end
    if output != nil
      return "#{output.upcase}"
    else
      find_output
    end
  end
  #
  def get_return(value,type="letter")
    alphabet=[nil,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    if type == 'letter'
      return alphabet[value]
    else
      #puts alphabet.index(value)
      return alphabet.index(value)
    end
  end
  def get_number(value)
    #
  end
  def get_value(card,type)
    #define values
    values={'clubs'=>0,'diamonds'=>13,'hearts'=>26,'spades'=>39,'ace'=>1,'jack'=>11,'queen'=>12,'king'=>13,'joker'=>53,'A'=>0,'B'=>0}
    facecards=['jack','queen','king','ace','joker']
    if type=='card'
     #
      suit,number=card.split('.')
      if facecards.include? number
        value=values[number]
      else
        value=number.to_i
      end
      value +=values[suit]
    else
      #
      if card < 14
        suit='clubs'
        number=card
      elsif card < 27
        suit='diamonds'
        number=card -13
      elsif card < 40
        suit='hearts'
        number=card -26
      else 
        suit='spades'
        number=card -39
      end
      if values.key(number)
        value="#{suit}.#{values.key(number)}"
      else
        value="#{suit}.#{number}"  
      end
     end     
    return value
  end
  
  def move_joker(jokerAB)
    old_position=@cards.index(jokerAB)
    if jokerAB =='joker.A'
      new_position=old_position + 1
    else
      new_position=old_position +2
    end 
    if new_position == 54
      new_position=1
    elsif new_position == 55
      new_position=2
    end
    @cards.delete_at(old_position)
    @cards[new_position, 0] = jokerAB
 
 end
  #
  def swap_two(one,two)
    @cards[one],@cards[two] = @cards[two],@cards[one]
  end  
  #
  def triple_cut
    #puts "triple_cut"
    topjoker,bottomjoker = [@cards.index('joker.A'),@cards.index('joker.B')].sort

      upper=@cards.slice!((bottomjoker +1)..-1)
      lower=@cards.slice!(0, topjoker)
      @cards= upper + @cards +lower
  end
  #
  def pick_a_card
    puts @cards.sample(1)
  end
  def print_deck
    @cards.each do |card|
      puts card
    end
  end
    
end #end class
#
#
def sanitize(string)
  # take string and uppercase, remove non alpha characters, and split in to five character segments (padded with XX)
  string.gsub!(/[^a-z]/i,'')
  return string.upcase
end
#
def generate_keystream(size)
  # take string, count characters and return keystring of same size
  keystream=[]
  size.times do
    keystream.push($hoyle.find_output().chomp)
  end
  keystream.delete(nil)
  return keystream
end
#
def crypt_message(string,action)
  #take message and encrypt
  # sanitize, convert to numbers, get keystream, convert keystream to numbers, add keystream subtract if > 26, convert to letters(in 5 char blocks(!!-- maybe do not split, leave that just for output??))
  sanitized=sanitize(string)
  letters=[]
  nospaces=[]
  numbers=[]
  numbersk=[]
  sanitized.each_char {|c| numbers.push($hoyle.get_return(c,'number') )}
  keystream=generate_keystream(sanitized.size)
  #puts sanitized, keystream
  keystream.each {|k| numbersk.push ($hoyle.get_return(k,'number') )}
  if action == 'encrypt'
    numbers.size.times do |num|
      #encrypt
      if numbers[num] + numbersk[num] > 26
        value=(numbers[num] + numbersk[num] - 26)
      else
        value=(numbers[num] + numbersk[num])
      end
      letters.push(value)
    end
  else
    numbers.size.times do |num|
      #decrypt
      if numbers[num] <= numbersk[num]
        value=((numbers[num] + 26) - numbersk[num] )
      else
        value=(numbers[num] - numbersk[num])
      end
        letters.push(value)
     end
  end
  letters.each {|l| nospaces.push($hoyle.get_return(l))}
  segments=(nospaces.size) / 5
  partial=(nospaces.size) % 5
  message=String.new
  segments.times do
    5.times do
      message.concat(nospaces.shift)
    end
    message.concat(' ')    
  end
  if partial > 0
    pad= 5 - partial
    partial.times do
      message.concat(nospaces.shift)
    end
    pad.times do
      message.concat('X')
    end
  end
  return message
end
#
#
#
$hoyle=Deck_of_cards.new
#puts crypt_message('GLNCQ MJAFF FVOMB JIYCB', 'decrypt')
#puts crypt_message('CODEI NRUBY LIVEL ONGER','encrypt')
# take input from command line
puts "Enter some text"
text=gets.chomp
puts "Do you want to encrypt or decrypt?"
action=gets.chomp
#puts action
while !(action == 'encrypt') and  !(action == 'decrypt')
  puts "Please choose either encrypt or decrypt"
  action=gets.chomp
end 
puts crypt_message(text,action) 




