#ifndef _VELODYNE_PLUGIN_HH_
#define _VELODYNE_PLUGIN_HH_

#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/Plugin.hh>
#include <rclcpp/rclcpp.hpp>
#include <memory>
#include <chrono>

using namespace std::chrono_literals;
namespace gazebo
{
  /// \brief A plugin to control a Velodyne sensor.
  class VelodynePlugin : public ModelPlugin
  {
    /// \brief Constructor
    public: 
    gazebo::event::ConnectionPtr update_connection_;
    int count_ = 0;
    // Pointer to the model
    gazebo::physics::ModelPtr parent_model_;

    VelodynePlugin() {
      


    }

    /// \brief The load function is called by Gazebo when the plugin is
    /// inserted into simulation
    /// \param[in] _model A pointer to the model that this plugin is
    /// attached to.
    /// \param[in] _sdf A pointer to the plugin's SDF element.
    public: 

    rclcpp::Time last_update_sim_time_ros_ = rclcpp::Time((int64_t)0, RCL_ROS_TIME);

    virtual void Load(physics::ModelPtr _model, sdf::ElementPtr _sdf)
    {
      parent_model_ = _model;
      this->update_connection_ = gazebo::event::Events::ConnectWorldUpdateBegin(
      std::bind(&VelodynePlugin::OnUpdate, this));
      // Just output a message for now
      std::cerr << "\nThe velodyne plugin is attach to model[" << "]\n";
    }
    virtual void Reset()
    {
      
      // Just output a message for now
      std::cerr << "\nThe velodyne plugin has been reset to model[" << "]\n";
    }
    virtual void OnUpdate()
    { 
      gazebo::common::Time gz_time_now = parent_model_->GetWorld()->SimTime();
      rclcpp::Time sim_time_ros(gz_time_now.sec, gz_time_now.nsec, RCL_ROS_TIME);
      // Just output a message for now
      last_update_sim_time_ros_ = sim_time_ros;
      count_++;
      //std::cerr << "Uddate data :"<< count_<<"]\n";
    }
  };

  // Tell Gazebo about this plugin, so that Gazebo can call Load on this plugin.
  GZ_REGISTER_MODEL_PLUGIN(VelodynePlugin)
}
#endif