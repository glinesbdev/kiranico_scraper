class Monster
  attr_accessor :name, :base_hp, :capture_hp, :small_crown, :silver_crown, :gold_crown, :quests, :hit_data

  def initialize
    @quests = []
    @hit_data = { elemental: [], breakage: [] }
  end
end