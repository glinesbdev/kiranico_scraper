require 'selenium-webdriver'
require 'ostruct'

require_relative './monster'
require_relative './csv_handler'
require_relative './xml_handler'

class MonsterScraper
  attr_reader :wait, :driver, :csv, :names, :monsters, :xml, :options, :browser, :format, :files

  def initialize monster_names
    @browser = ARGV[0] ||= 'firefox'
    @format = ARGV[1] ||= 'xml'
    @files = { xml: './data/monsters.xml', csv: './data/monsters.csv' }

    setup_browser

    @wait = Selenium::WebDriver::Wait.new(timeout: 120)
    @monsters = []
    @names = monster_names

    Dir.mkdir './data' unless File.exists? './data'

    @csv = CSVHandler.new "#{files[:csv]}"
    @xml = XMLHandler.new "#{files[:xml]}"
  end

  def setup_browser
    if @browser == '--help' || @browser == '-h'
      write_help
      exit
    end

    if @browser == 'chrome'
      setup_chrome
    elsif @browser == 'firefox'
      setup_firefox
    end
  end

  def setup_chrome
    @options = Selenium::WebDriver::Chrome::Options.new(args: ['--headless', '--ignore-certificate-errors', '--no-sandbox', '--disable-extensions', '--disable-gpu'])
    @driver = Selenium::WebDriver.for(:chrome, options: @options)
  end

  def setup_firefox
    @options = Selenium::WebDriver::Firefox::Options.new(args: ['--headless', '--disable-extensions'])
    @driver = Selenium::WebDriver.for(:firefox, options: @options)
  end

  def build_monsters
    @names.each do |name|
      @monster = Monster.new
      @driver.get("https://mhworld.kiranico.com/monster/#{name}")

      @monster.name = name.capitalize
      @monster.base_hp = monster_basics[0].text.strip
      @monster.capture_hp = monster_basics[1].text.strip
      @monster.small_crown = monster_basics[2].text.strip
      @monster.silver_crown = monster_basics[3].text.strip
      @monster.gold_crown = monster_basics[4].text.strip
      @monster.quests = quests

      hit_data @monster
      hit_data_breakage @monster

      @driver.close

      if @format == 'xml'
        write_xml @monster
      elsif @format == 'csv'
        write_csv @monster
      end
    end
  end

  def monster_basics
    elements = @wait.until {
      items = @driver.find_elements(css: '.p-3.text-center .lead')
      items if items.first.displayed?
    }
  end

  def quests
    quest_names = []

    item = @driver.find_elements(class: 'card-body')[2]
    item.find_elements(css: 'table a').each do |link|
      quest_names << link.text.strip
    end

    quest_names
  end

  def hit_data monster
    item = @driver.find_elements(class: 'card-body')[3]
    col = item.find_element(class: 'col-sm-8')
    rows = col.find_elements(css: 'table tbody tr')

    rows.each do |row|
      monster_data = OpenStruct.new
      data = row.find_elements(css: 'td')

      monster_data.name = data[0].text.strip
      monster_data.sever = data[1].text.strip
      monster_data.blunt = data[2].text.strip
      monster_data.shot = data[3].text.strip
      monster_data.fire = data[4].text.strip
      monster_data.water = data[5].text.strip
      monster_data.thunder = data[6].text.strip
      monster_data.ice = data[7].text.strip
      monster_data.dragon = data[8].text.strip
      monster_data.stun = data[9].text.strip      

      monster.hit_data[:elemental] << monster_data
    end
  end

  def hit_data_breakage monster
    item = @driver.find_elements(class: 'card-body')[3]
    col = item.find_element(class: 'col-sm-4')
    rows = col.find_elements(css: 'table tbody tr')

    rows.each do |row|
      monster_data = OpenStruct.new
      data = row.find_elements(css: 'td')

      monster_data.name = data[0].text.strip
      monster_data.flinch = data[1].text.strip
      monster_data.wound = data[2].text.strip
      monster_data.sever = data[3].text.strip

      monster.hit_data[:breakage] << monster_data
    end
  end

  def write_csv monster
    begin
      @csv.write(@csv.generate_monster_csv monster)
    rescue Exception => e
      puts "Rescued with error: #{e.message}"
      @driver.quit
      exit
    end
  end

  def write_xml monster
    begin
      @xml.write(@xml.generate_monster_xml monster)
    rescue Exception => e
      puts "Rescued with error: #{e.message}"
      @driver.quit
      exit
    end
  end

  def write_help
    puts "Accepted browser arguments: firefox, chrome"
    puts "Accepted format arguments: csv, xml"
    puts "Ex: ruby monster_scraper.rb [chrome, (firefox: default)] [(xml: default), csv]"
    puts "Giving no arguments will run Firefox and create an XML file in the ./data/ folder"
  end

end

scraper = MonsterScraper.new(['anjanath'])
scraper.build_monsters