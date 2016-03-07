class Deck_of_cards
  def initialize
    #define values
    clubs=0
    diamonds=13
    hearts=26
    spades=39
    ace=1
    jack=11
    queen=12
    king=13
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
    #puts @cards.length
    #shuffle
  end # end initialize
  def shuffle
    # actually prepare the deck for encryption
    move_joker('joker.A',1)
    move_joker('joker.B',2)
    triple_cut
    #count_cut
  end
  def move_joker(jokerAB,offset)
    old_position=@cards.index(jokerAB)
    new_position=old_position + offset
    #puts new_position
    if new_position == 55
      new_position=1
    elsif new_position == 56
      new_position=2
    end
    @cards[old_position],@cards[new_position] = @cards[new_position],@cards[old_position] 
    wtf=@cards.index('joker.A')
    fuck=@cards.index('joker.B')   
    puts " joker a is at #{wtf} , joker b is at #{fuck}"
  end
  def rotate_whole_deck
    (54..1).each do |n|
      saveit=@cards[n-1]
      if (n-1) !=0
        @cards[n-1] = @cards[n]
      else
        @cards[54]=@cards[0]
        @cards[0]=@cards[1]
      end
    end  
  end  
  def swap_two(one,two)
    @cards[one],@cards[two] = @cards[two],@cards[one]
  end  
  def triple_cut
    jokerA_pos=@cards.index('joker.A')
    jokerB_pos=@cards.index('joker.B')
    if @cards.index('joker.A') > @cards.index('joker.B')
      topjoker='joker.B'
      bottomjoker='joker.A'
    else
      topjoker='joker.A'
      bottomjoker='joker.B'
    end
    # add check for topjoker !@position 0
    card2=@cards.index(bottomjoker) +1
    if @cards.index(topjoker) <= (54 - @cards.index(bottomjoker))
      (0..@cards.index(topjoker)).each do |card|
        swap_two(card,card2)
        card2=card2+1
      end
      else
        rotate_whole_deck
      end

    #@cards.each
  end
  def pick_a_card
    puts @cards.sample(1)
  end
  def print_deck
    @cards.each do |card|
      puts card
    end
  end
    
end #end class

hoyle=Deck_of_cards.new
#variable=hoyle.pick_a_card
hoyle.print_deck
hoyle.shuffle
hoyle.print_deck
