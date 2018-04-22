require 'csv'

class CSVHandler
  attr_accessor :file_name
  attr_reader :monster_headers

  def initialize file_name
    @file_name = file_name
    @monster_headers = ['Name', 'Base HP', 'Capture HP', 'Small Crown', 'Silver Crown', 'Gold Crown', 'Quests']
  end

  def generate_monster_csv monster
    data = CSV.generate do |csv|
      quests = []
      csv << @monster_headers
      csv << [monster.name, monster.base_hp, monster.capture_hp, monster.small_crown, monster.silver_crown, monster.gold_crown]

      monster.quests.each do |quest|
        quest = "#{quest}|" unless quest == monster.quests.last
        quests << quest
      end

      csv << quests
    end

    data
  end

  def write csv
    File.open(@file_name, 'a:UTF-8') { |file| file.write(csv) }
  end

end