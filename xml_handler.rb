require 'nokogiri'

class XMLHandler

  attr_reader :doc, :file_name, :monster

  def initialize file
    @file_name = file
    @doc = Nokogiri::XML('<Monsters></Monsters>')
    @monster = Nokogiri::XML::Node.new 'Monster', @doc
  end

  def generate_monster_xml monster
    @monster << "<Name>#{monster.name}</Name>"
    @monster << "<BaseHp>#{monster.base_hp}</BaseHp>"
    @monster << "<CaptureHp>#{monster.capture_hp}</CaptureHp>"
    @monster << "<SmallCrown>#{monster.small_crown}</SmallCrown>"
    @monster << "<SilverCrown>#{monster.silver_crown}</SilverCrown>"
    @monster << "<GoldCrown>#{monster.gold_crown}</GoldCrown>"

    quests = Nokogiri::XML::Node.new 'Quests', @doc

    if monster.quests.any?
      monster.quests.each { |quest| quests << "<Quest>#{quest}</Quest>" }
      @monster << quests
    end

    hit_data = Nokogiri::XML::Node.new 'HitData', @doc

    if monster.hit_data[:elemental].any?
      elemental = Nokogiri::XML::Node.new 'Elemental', @doc

      monster.hit_data[:elemental].each do |hit|
        part = Nokogiri::XML::Node.new hit.name, @doc
        part << "<Sever>#{hit.sever}</Sever>"
        part << "<Blunt>#{hit.blunt}</Blunt>"
        part << "<Shot>#{hit.shot}</Shot>"
        part << "<Fire>#{hit.fire}</Fire>"
        part << "<Water>#{hit.water}</Water>"
        part << "<Thunder>#{hit.thunder}</Thunder>"
        part << "<Ice>#{hit.ice}</Ice>"
        part << "<Dragon>#{hit.dragon}</Dragon>"
        part << "<Stun>#{hit.stun}</Stun>"

        elemental << part
      end

      hit_data << elemental
    end

    if monster.hit_data[:breakage].any?
      breakage = Nokogiri::XML::Node.new 'Breakage', @doc

      monster.hit_data[:breakage].each do |hit|
        part = Nokogiri::XML::Node.new hit.name, @doc
        part << "<Flinch>#{hit.flinch}</Flinch>"
        part << "<Wound>#{hit.wound}</Wound>"
        part << "<Sever>#{hit.sever}</Sever>"

        breakage << part
      end

      hit_data << breakage
    end

    @monster << hit_data
    @doc.root << @monster
    @doc.to_xml
  end

  def write xml
    File.open(@file_name, 'a:UTF-8') { |file| file.write xml }
  end

end