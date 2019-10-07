!*******************************************************************************
!
!  Routine:     EvolveProtostellar
!
!  Description: Evolution subroutine for the protostellar_evolution sub-module.
!               Evolves the radius and luminosity of the sink particles so that
!               radiation codes can accurately determine feedback.
!
!  Written:     Mikhail Klassen 2010 (McMaster University)
!  Updated:     Mikhail Klassen 2011 (McMaster University)
!  ...    :     Mikhail Klassen 2014 (McMaster University)
!
!*******************************************************************************

program TurbulentCoreDriver

    use protostellar_interface, only: star, Msun, Rsun, secyr

    implicit none

    double precision :: dt
    double precision :: mdot
    double precision :: time, maxtime
    double precision :: mfinal, mdot1, tf1, tf

    ! Initialize our star
    star%mass   = 0.001 * Msun ! need to start with some initial mass to set accr. rate
    star%mdot   = 0.0
    star%radius = 0.0
    star%polyn  = 0.0
    star%mdeut  = 0.0
    star%lint   = 0.0
    star%lum    = 0.0
    star%stage  = 0

    ! set the final mass, which determines the accretion rate etc. below
    mfinal = 2.906000E+00

    ! compute tfinal from mfinal
    mdot1 = 4.9e-6 ! normalized by surface density^3/4
    tf1 = 2./mdot1
    tf = tf1 * mfinal**(0.25)

    ! Set the initial accretion rate (grams per second)
    mdot = mdot1 * (star%mass/Msun/mfinal)**0.5 * mfinal**0.75 * Msun / secyr
    star%mdot = mdot

    ! Set the timestep (seconds)
    dt = 10000.000000 * secyr

    ! Initialize the simulation time and set the maxtime
    time = 0.0
    maxtime = 2.000000E+06 * secyr

    ! Open file for writing
    open(unit=1, file="turbulentcore_protostellar_evolution.txt", action="write")
    write(1,FMT=101) 'Time','Stellar_Mass','Accretion_Rate','Stellar_Radius','Polytropic_Index',&
                     'Deuterium_Mass','Intrinsic_Lum','Total_Luminosity','Stage'

    ! Evolve the star
    do while(time < maxtime)
        call EvolveProtostellar(dt)
        star%mass = star%mass + star%mdot*dt

        !if (time < tf * secyr) then
        if (star%mass/Msun < mfinal) then
            ! update the mass accretion rate
            mdot = mdot1 * (star%mass/Msun/mfinal)**0.5 * mfinal**0.75 * Msun / secyr
            star%mdot = mdot
        else
            ! stop accretion once target time (mass) has been hit
            star%mdot = 0
        endif
        

        time = time + dt
        write(1,FMT=100) time, star%mass, star%mdot, star%radius, &
                        & star%polyn, star%mdeut, star%lint, &
                        & star%lum, star%stage
    end do

    ! Close the file
    close(1)

    print *, 'Simulation reach max time.'

    ! Format statement
    100 format (8(E17.10,3X),I6)
    101 format (8(A17,3X),A6)

end program TurbulentCoreDriver
